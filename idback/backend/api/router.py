import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import List, Optional

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.http import HttpRequest
from ninja import NinjaAPI, Query, Router

from api.auth import (
    GlobalAuth,
    create_token_for_user,
    delete_user_tokens,
    editor_required,
    subscriber_required,
    writer_required,
)
from users.models import (
    Subscription,
    SubscriptionPlan,
)
from common.models import Article, Category, Edition, PrintOrder
from api.schemas import (
    ArticleBrief,
    ArticleCreate,
    ArticleOut,
    ArticleStatusUpdate,
    ArticleUpdate,
    AuthorBrief,
    AuthorCreate,
    AuthorOut,
    AuthorUpdate,
    CategoryBrief,
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    EditionBrief,
    EditionCreate,
    EditionOut,
    EditionUpdate,
    EditorialActivityOut,
    EditorialQueueItemOut,
    EditorialStatsOut,
    HomepageData,
    MessageOut,
    PaginatedResponse,
    PrintOrderCreate,
    PrintOrderOut,
    PrintPricingOut,
    SearchFilters,
    SubscriptionCreate,
    SubscriptionOut,
    SubscriptionPlanOut,
    TokenOut,
    UserLogin,
    UserOut,
    UserRegister,
)

User = get_user_model()

api = NinjaAPI(title="MERIDIAN Magazine API", version="1.0.0")

# ============================================================
# Helper functions
# ============================================================


def _build_article_brief(article: Article) -> ArticleBrief:
    return ArticleBrief(
        id=str(article.id),
        title=article.title,
        slug=article.slug,
        excerpt=article.excerpt,
        cover_image=article.cover_image.url if article.cover_image else "",
        author_name=article.author.name,
        author_slug=article.author.slug,
        category_name=article.category.name,
        category_slug=article.category.slug,
        published_at=article.published_at,
        reading_time=article.reading_time,
        content_type=article.content_type,
        access=article.access,
        featured=article.featured,
        trending=article.trending,
        pinned=article.pinned,
    )


def _build_article_out(article: Article) -> ArticleOut:
    return ArticleOut(
        id=str(article.id),
        title=article.title,
        slug=article.slug,
        subtitle=article.subtitle,
        content=article.content,
        excerpt=article.excerpt,
        cover_image=article.cover_image.url if article.cover_image else "",
        cover_caption=article.cover_caption,
        author=AuthorBrief(
            id=str(article.author.id),
            name=article.author.name,
            slug=article.author.slug,
            avatar=article.author.avatar.url if article.author.avatar else "",
            role=article.author.role,
        ),
        category=CategoryBrief(
            id=article.category.id,
            name=article.category.name,
            slug=article.category.slug,
            color=article.category.color,
            access=article.category.access,
        ),
        content_type=article.content_type,
        access=article.access,
        status=article.status,
        seo_title=article.seo_title,
        seo_description=article.seo_description,
        seo_keywords=article.seo_keywords or [],
        published_at=article.published_at,
        updated_at=article.updated_at,
        created_at=article.created_at,
        reading_time=article.reading_time,
        word_count=article.word_count,
        featured=article.featured,
        trending=article.trending,
        pinned=article.pinned,
        reviewed_by_name=article.reviewed_by.name if article.reviewed_by else None,
        rejection_reason=article.rejection_reason,
    )


def _build_edition_brief(edition: Edition) -> EditionBrief:
    return EditionBrief(
        id=str(edition.id),
        number=edition.number,
        title=edition.title,
        slug=edition.slug,
        cover_image=edition.cover_image.url if edition.cover_image else "",
        status=edition.status,
        published_at=edition.published_at,
        week_start=edition.week_start,
        week_end=edition.week_end,
        article_count=edition.article_count,
    )


def _build_edition_out(edition: Edition) -> EditionOut:
    featured = None
    if edition.featured_article:
        featured = _build_article_brief(edition.featured_article)

    articles = [_build_article_brief(a) for a in edition.articles.all()]

    return EditionOut(
        id=str(edition.id),
        number=edition.number,
        title=edition.title,
        subtitle=edition.subtitle,
        slug=edition.slug,
        cover_image=edition.cover_image.url if edition.cover_image else "",
        status=edition.status,
        published_at=edition.published_at,
        week_start=edition.week_start,
        week_end=edition.week_end,
        featured_article=featured,
        print_ready=edition.print_ready,
        print_pdf_url=edition.print_pdf_url.url if edition.print_pdf_url else "",
        article_count=edition.article_count,
        articles=articles,
        created_at=edition.created_at,
        updated_at=edition.updated_at,
    )


def _paginate(queryset, page: int, page_size: int, request: HttpRequest):
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    base_url = request.build_absolute_uri(request.path)
    next_url = None
    previous_url = None
    if page_obj.has_next():
        next_url = (
            f"{base_url}?page={page_obj.next_page_number()}&page_size={page_size}"
        )
    if page_obj.has_previous():
        previous_url = (
            f"{base_url}?page={page_obj.previous_page_number()}&page_size={page_size}"
        )
    return page_obj, next_url, previous_url


# ============================================================
# Public Routes
# ============================================================

# --- Articles ---


@api.get("/articles/", response=PaginatedResponse[ArticleBrief])
def list_articles(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category: Optional[str] = Query(None),
    access: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    trending: Optional[bool] = Query(None),
    author: Optional[str] = Query(None),
):
    qs = Article.objects.filter(status=Article.Status.PUBLISHED).select_related(
        "author", "category"
    )
    if category:
        qs = qs.filter(category__slug=category)
    if access:
        qs = qs.filter(access=access)
    if featured is not None:
        qs = qs.filter(featured=featured)
    if trending is not None:
        qs = qs.filter(trending=trending)
    if author:
        qs = qs.filter(author__slug=author)
    qs = qs.order_by("-published_at")

    page_obj, next_url, previous_url = _paginate(qs, page, page_size, request)
    results = [_build_article_brief(a) for a in page_obj]
    return PaginatedResponse(
        count=page_obj.paginator.count,
        next=next_url,
        previous=previous_url,
        results=results,
    )


@api.get("/articles/{slug}", response=ArticleOut)
def get_article(request: HttpRequest, slug: str):
    article = (
        Article.objects.filter(slug=slug, status=Article.Status.PUBLISHED)
        .select_related("author", "category", "reviewed_by")
        .first()
    )
    if not article:
        from ninja.errors import HttpError

        raise HttpError(404, "Article not found")
    return _build_article_out(article)


# --- Categories ---


@api.get("/categories/", response=List[CategoryOut])
def list_categories(request: HttpRequest):
    cats = Category.objects.all().order_by("name")
    return [
        CategoryOut(
            id=c.id,
            name=c.name,
            slug=c.slug,
            description=c.description,
            color=c.color,
            access=c.access,
            icon=c.icon,
            featured=c.featured,
            article_count=c.article_count,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in cats
    ]


@api.get("/categories/{slug}", response=CategoryOut)
def get_category(request: HttpRequest, slug: str):
    cat = Category.objects.filter(slug=slug).first()
    if not cat:
        from ninja.errors import HttpError

        raise HttpError(404, "Category not found")
    return CategoryOut(
        id=cat.id,
        name=cat.name,
        slug=cat.slug,
        description=cat.description,
        color=cat.color,
        access=cat.access,
        icon=cat.icon,
        featured=cat.featured,
        article_count=cat.article_count,
        created_at=cat.created_at,
        updated_at=cat.updated_at,
    )


# --- Authors ---


@api.get("/authors/", response=List[AuthorOut])
def list_authors(request: HttpRequest):
    authors = Author.objects.all().order_by("name")
    return [
        AuthorOut(
            id=str(a.id),
            name=a.name,
            slug=a.slug,
            bio=a.bio,
            avatar=a.avatar.url if a.avatar else "",
            role=a.role,
            twitter=a.twitter,
            linkedin=a.linkedin,
            instagram=a.instagram,
            website=a.website,
            article_count=a.article_count,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )
        for a in authors
    ]


@api.get("/authors/{slug}", response=AuthorOut)
def get_author(request: HttpRequest, slug: str):
    author = Author.objects.filter(slug=slug).first()
    if not author:
        from ninja.errors import HttpError

        raise HttpError(404, "Author not found")
    return AuthorOut(
        id=str(author.id),
        name=author.name,
        slug=author.slug,
        bio=author.bio,
        avatar=author.avatar.url if author.avatar else "",
        role=author.role,
        twitter=author.twitter,
        linkedin=author.linkedin,
        instagram=author.instagram,
        website=author.website,
        article_count=author.article_count,
        created_at=author.created_at,
        updated_at=author.updated_at,
    )


# --- Editions ---


@api.get("/editions/", response=PaginatedResponse[EditionBrief])
def list_editions(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
):
    qs = Edition.objects.filter(status=Edition.Status.PUBLISHED).order_by("-number")
    page_obj, next_url, previous_url = _paginate(qs, page, page_size, request)
    results = [_build_edition_brief(e) for e in page_obj]
    return PaginatedResponse(
        count=page_obj.paginator.count,
        next=next_url,
        previous=previous_url,
        results=results,
    )


@api.get("/editions/{slug}", response=EditionOut)
def get_edition(request: HttpRequest, slug: str):
    edition = (
        Edition.objects.filter(slug=slug)
        .prefetch_related("articles__author", "articles__category")
        .first()
    )
    if not edition:
        from ninja.errors import HttpError

        raise HttpError(404, "Edition not found")
    return _build_edition_out(edition)


@api.get("/editions/latest/", response=EditionOut)
def get_latest_edition(request: HttpRequest):
    edition = (
        Edition.objects.filter(status=Edition.Status.PUBLISHED)
        .prefetch_related(
            "articles__author",
            "articles__category",
            "featured_article__author",
            "featured_article__category",
        )
        .order_by("-number")
        .first()
    )
    if not edition:
        from ninja.errors import HttpError

        raise HttpError(404, "No published editions found")
    return _build_edition_out(edition)


# --- Search ---


@api.get("/search/", response=PaginatedResponse[ArticleBrief])
def search_articles(
    request: HttpRequest,
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category: Optional[str] = Query(None),
):
    qs = Article.objects.filter(status=Article.Status.PUBLISHED).select_related(
        "author", "category"
    )
    qs = qs.filter(
        Q(title__icontains=q)
        | Q(excerpt__icontains=q)
        | Q(content__icontains=q)
        | Q(seo_keywords__icontains=q)
    )
    if category:
        qs = qs.filter(category__slug=category)
    qs = qs.order_by("-published_at")

    page_obj, next_url, previous_url = _paginate(qs, page, page_size, request)
    results = [_build_article_brief(a) for a in page_obj]
    return PaginatedResponse(
        count=page_obj.paginator.count,
        next=next_url,
        previous=previous_url,
        results=results,
    )


# --- Homepage Bundle ---


@api.get("/homepage/", response=HomepageData)
def get_homepage(request: HttpRequest):
    published = Article.objects.filter(status=Article.Status.PUBLISHED).select_related(
        "author", "category"
    )
    featured = list(published.filter(featured=True).order_by("-published_at")[:6])
    trending = list(published.filter(trending=True).order_by("-published_at")[:6])
    pinned = list(published.filter(pinned=True).order_by("-published_at")[:5])

    latest_ed = (
        Edition.objects.filter(status=Edition.Status.PUBLISHED)
        .order_by("-number")
        .first()
    )
    categories = list(Category.objects.filter(featured=True).order_by("name"))

    return HomepageData(
        featured_articles=[_build_article_brief(a) for a in featured],
        trending_articles=[_build_article_brief(a) for a in trending],
        pinned_articles=[_build_article_brief(a) for a in pinned],
        latest_edition=_build_edition_brief(latest_ed) if latest_ed else None,
        categories=[
            CategoryBrief(
                id=c.id, name=c.name, slug=c.slug, color=c.color, access=c.access
            )
            for c in categories
        ],
    )


# --- Subscription Plans ---


@api.get("/plans/", response=List[SubscriptionPlanOut])
def list_plans(request: HttpRequest):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by("price")
    return [
        SubscriptionPlanOut(
            id=p.id,
            name=p.name,
            plan_type=p.plan_type,
            price=float(p.price),
            currency=p.currency,
            interval=p.interval,
            features=p.features or [],
            highlighted=p.highlighted,
            print_included=p.print_included,
            is_active=p.is_active,
        )
        for p in plans
    ]


# --- Print Pricing ---


@api.get("/print/pricing/", response=PrintPricingOut)
def get_print_pricing(request: HttpRequest):
    return PrintPricingOut(
        unit_price_us=12.99,
        shipping_us=4.99,
        unit_price_international=14.99,
        shipping_international=12.99,
        bulk_discount_threshold=5,
        bulk_discount_percent=10.0,
        currency="USD",
    )


# ============================================================
# Auth Routes
# ============================================================


@api.post("/auth/register/", response=TokenOut)
def register(request: HttpRequest, data: UserRegister):
    if User.objects.filter(username=data.username).exists():
        from ninja.errors import HttpError

        raise HttpError(400, "Username already exists")
    if User.objects.filter(email=data.email).exists():
        from ninja.errors import HttpError

        raise HttpError(400, "Email already exists")

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        role=User.Role.VISITOR,
    )
    token = create_token_for_user(user)
    return TokenOut(
        token=token.key,
        user_id=str(user.id),
        username=user.username,
        role=user.role,
    )


@api.post("/auth/login/", response=TokenOut)
def login(request: HttpRequest, data: UserLogin):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        from ninja.errors import HttpError

        raise HttpError(401, "Invalid credentials")
    if not user.is_active:
        from ninja.errors import HttpError

        raise HttpError(401, "Account disabled")

    delete_user_tokens(user)
    token = create_token_for_user(user)
    return TokenOut(
        token=token.key,
        user_id=str(user.id),
        username=user.username,
        role=user.role,
    )


@api.get("/auth/me/", response=UserOut, auth=GlobalAuth())
def get_current_user(request: HttpRequest):
    user = request.auth
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        date_joined=user.date_joined,
    )


# ============================================================
# Writer Routes (role=writer required)
# ============================================================


@api.post("/articles/", response=ArticleOut, auth=GlobalAuth())
def create_article(request: HttpRequest, data: ArticleCreate):
    user = writer_required(request.auth)
    author = Author.objects.filter(user=user).first()
    if not author:
        from ninja.errors import HttpError

        raise HttpError(400, "User does not have an author profile")

    category = Category.objects.filter(id=data.category_id).first()
    if not category:
        from ninja.errors import HttpError

        raise HttpError(404, "Category not found")

    article = Article.objects.create(
        title=data.title,
        slug=data.slug,
        subtitle=data.subtitle,
        content=data.content,
        excerpt=data.excerpt,
        cover_image=data.cover_image,
        cover_caption=data.cover_caption,
        author=author,
        category=category,
        content_type=data.content_type,
        access=data.access,
        seo_title=data.seo_title,
        seo_description=data.seo_description,
        seo_keywords=data.seo_keywords,
        reading_time=data.reading_time,
        word_count=data.word_count,
        featured=data.featured,
        trending=data.trending,
        status=Article.Status.DRAFT,
    )

    EditorialActivity.objects.create(
        article=article,
        action=EditorialActivity.Action.CREATED,
        performed_by=user,
        details="Article created as draft",
    )

    return _build_article_out(
        Article.objects.select_related("author", "category", "reviewed_by").get(
            pk=article.pk
        )
    )


@api.put("/articles/{article_id}", response=ArticleOut, auth=GlobalAuth())
def update_article(request: HttpRequest, article_id: str, data: ArticleUpdate):
    user = writer_required(request.auth)
    try:
        article = Article.objects.select_related(
            "author", "category", "reviewed_by"
        ).get(pk=article_id)
    except Article.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Article not found")

    if (
        article.author.user != user
        and user.role != User.Role.EDITOR
        and user.role != User.Role.ADMIN
    ):
        from ninja.errors import HttpError

        raise HttpError(403, "You can only edit your own articles")

    update_fields = data.model_dump(exclude_unset=True)
    if "category_id" in update_fields:
        cat = Category.objects.filter(id=update_fields.pop("category_id")).first()
        if not cat:
            from ninja.errors import HttpError

            raise HttpError(404, "Category not found")
        article.category = cat

    for field, value in update_fields.items():
        setattr(article, field, value)
    article.save()

    EditorialActivity.objects.create(
        article=article,
        action=EditorialActivity.Action.EDITED,
        performed_by=user,
        details="Article updated",
    )

    return _build_article_out(
        Article.objects.select_related("author", "category", "reviewed_by").get(
            pk=article.pk
        )
    )


@api.delete("/articles/{article_id}", response=MessageOut, auth=GlobalAuth())
def delete_article(request: HttpRequest, article_id: str):
    user = writer_required(request.auth)
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Article not found")

    if article.author.user != user and user.role != User.Role.ADMIN:
        from ninja.errors import HttpError

        raise HttpError(403, "You can only delete your own articles")

    if article.status != Article.Status.DRAFT:
        from ninja.errors import HttpError

        raise HttpError(400, "Only draft articles can be deleted")

    article.delete()
    return MessageOut(message="Article deleted successfully")


@api.post("/articles/{article_id}/submit/", response=ArticleOut, auth=GlobalAuth())
def submit_article(request: HttpRequest, article_id: str):
    user = writer_required(request.auth)
    try:
        article = Article.objects.select_related(
            "author", "category", "reviewed_by"
        ).get(pk=article_id)
    except Article.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Article not found")

    if article.author.user != user and user.role != User.Role.ADMIN:
        from ninja.errors import HttpError

        raise HttpError(403, "You can only submit your own articles")

    if article.status not in (Article.Status.DRAFT, Article.Status.REJECTED):
        from ninja.errors import HttpError

        raise HttpError(400, "Only draft or rejected articles can be submitted")

    article.status = Article.Status.IN_REVIEW
    article.rejection_reason = ""
    article.save()

    EditorialActivity.objects.create(
        article=article,
        action=EditorialActivity.Action.SUBMITTED,
        performed_by=user,
        details="Article submitted for editorial review",
    )

    return _build_article_out(
        Article.objects.select_related("author", "category", "reviewed_by").get(
            pk=article.pk
        )
    )


# ============================================================
# Editor Routes (role=editor required)
# ============================================================


@api.patch("/articles/{article_id}/status/", response=ArticleOut, auth=GlobalAuth())
def update_article_status(
    request: HttpRequest, article_id: str, data: ArticleStatusUpdate
):
    user = editor_required(request.auth)
    try:
        article = Article.objects.select_related(
            "author", "category", "reviewed_by"
        ).get(pk=article_id)
    except Article.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Article not found")

    valid_transitions = {
        Article.Status.APPROVED,
        Article.Status.REJECTED,
        Article.Status.PUBLISHED,
    }
    if data.status not in valid_transitions:
        from ninja.errors import HttpError

        raise HttpError(400, f"Status must be one of: {', '.join(valid_transitions)}")

    if data.status == Article.Status.REJECTED and not data.rejection_reason:
        from ninja.errors import HttpError

        raise HttpError(400, "Rejection reason is required when rejecting an article")

    if data.status == Article.Status.PUBLISHED:
        article.published_at = datetime.now(timezone.utc)

    article.status = data.status
    if data.status == Article.Status.REJECTED:
        article.rejection_reason = data.rejection_reason
    if data.status in (
        Article.Status.APPROVED,
        Article.Status.REJECTED,
        Article.Status.PUBLISHED,
    ):
        article.reviewed_by = Author.objects.filter(user=user).first()
    article.save()

    EditorialActivity.objects.create(
        article=article,
        action=data.status,
        performed_by=user,
        details=f"Article {data.status}"
        + (f": {data.rejection_reason}" if data.rejection_reason else ""),
    )

    return _build_article_out(
        Article.objects.select_related("author", "category", "reviewed_by").get(
            pk=article.pk
        )
    )


@api.get(
    "/editorial/queue/",
    response=PaginatedResponse[EditorialQueueItemOut],
    auth=GlobalAuth(),
)
def editorial_queue(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
):
    editor_required(request.auth)
    qs = Article.objects.select_related("author", "category", "reviewed_by").order_by(
        "-updated_at"
    )
    if status:
        qs = qs.filter(status=status)

    page_obj, next_url, previous_url = _paginate(qs, page, page_size, request)
    results = [
        EditorialQueueItemOut(
            id=str(a.id),
            title=a.title,
            author_name=a.author.name,
            author_slug=a.author.slug,
            category_name=a.category.name,
            category_slug=a.category.slug,
            cover_image=a.cover_image.url if a.cover_image else "",
            excerpt=a.excerpt,
            status=a.status,
            submitted_at=a.updated_at,
            updated_at=a.updated_at,
            reviewed_by_name=a.reviewed_by.name if a.reviewed_by else None,
            rejection_reason=a.rejection_reason,
            word_count=a.word_count,
            reading_time=a.reading_time,
        )
        for a in page_obj
    ]
    return PaginatedResponse(
        count=page_obj.paginator.count,
        next=next_url,
        previous=previous_url,
        results=results,
    )


@api.get("/editorial/stats/", response=EditorialStatsOut, auth=GlobalAuth())
def editorial_stats(request: HttpRequest):
    editor_required(request.auth)
    total = Article.objects.count()
    drafts = Article.objects.filter(status=Article.Status.DRAFT).count()
    in_review = Article.objects.filter(status=Article.Status.IN_REVIEW).count()
    approved = Article.objects.filter(status=Article.Status.APPROVED).count()
    rejected = Article.objects.filter(status=Article.Status.REJECTED).count()
    published_week = Article.objects.filter(
        status=Article.Status.PUBLISHED,
        published_at__gte=datetime.now(timezone.utc) - timedelta(days=7),
    ).count()
    avg_rt = Article.objects.aggregate(avg=Avg("reading_time"))["avg"] or 0

    return EditorialStatsOut(
        total_drafts=drafts,
        in_review=in_review,
        approved=approved,
        rejected=rejected,
        published_this_week=published_week,
        total_articles=total,
        avg_reading_time=int(round(avg_rt)),
    )


@api.get("/editorial/activity/", response=List[EditorialActivityOut], auth=GlobalAuth())
def editorial_activity_log(
    request: HttpRequest,
    limit: int = Query(20, ge=1, le=100),
):
    editor_required(request.auth)
    activities = EditorialActivity.objects.select_related(
        "article", "performed_by"
    ).order_by("-created_at")[:limit]
    return [
        EditorialActivityOut(
            id=str(a.id),
            action=a.action,
            article_title=a.article.title,
            performed_by_name=a.performed_by.username,
            timestamp=a.created_at,
            details=a.details,
        )
        for a in activities
    ]


@api.post("/editions/", response=EditionOut, auth=GlobalAuth())
def create_edition(request: HttpRequest, data: EditionCreate):
    editor_required(request.auth)
    featured_article = None
    if data.featured_article_id:
        featured_article = Article.objects.filter(pk=data.featured_article_id).first()

    edition = Edition.objects.create(
        number=data.number,
        title=data.title,
        subtitle=data.subtitle,
        slug=data.slug,
        week_start=data.week_start,
        week_end=data.week_end,
        featured_article=featured_article,
        print_ready=data.print_ready,
        status=Edition.Status.DRAFT,
    )
    return _build_edition_out(
        Edition.objects.prefetch_related("articles__author", "articles__category").get(
            pk=edition.pk
        )
    )


@api.put("/editions/{edition_id}", response=EditionOut, auth=GlobalAuth())
def update_edition(request: HttpRequest, edition_id: str, data: EditionUpdate):
    editor_required(request.auth)
    try:
        edition = Edition.objects.get(pk=edition_id)
    except Edition.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Edition not found")

    update_fields = data.model_dump(exclude_unset=True)
    if "featured_article_id" in update_fields:
        fa_id = update_fields.pop("featured_article_id")
        edition.featured_article = (
            Article.objects.filter(pk=fa_id).first() if fa_id else None
        )

    for field, value in update_fields.items():
        setattr(edition, field, value)
    edition.save()

    return _build_edition_out(
        Edition.objects.prefetch_related("articles__author", "articles__category").get(
            pk=edition.pk
        )
    )


@api.delete("/editions/{edition_id}", response=MessageOut, auth=GlobalAuth())
def delete_edition(request: HttpRequest, edition_id: str):
    editor_required(request.auth)
    try:
        edition = Edition.objects.get(pk=edition_id)
    except Edition.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Edition not found")

    edition.delete()
    return MessageOut(message="Edition deleted successfully")


@api.post("/editions/{edition_id}/publish/", response=EditionOut, auth=GlobalAuth())
def publish_edition(request: HttpRequest, edition_id: str):
    editor_required(request.auth)
    try:
        edition = Edition.objects.get(pk=edition_id)
    except Edition.DoesNotExist:
        from ninja.errors import HttpError

        raise HttpError(404, "Edition not found")

    edition.status = Edition.Status.PUBLISHED
    edition.published_at = datetime.now(timezone.utc)
    edition.save()

    return _build_edition_out(
        Edition.objects.prefetch_related("articles__author", "articles__category").get(
            pk=edition.pk
        )
    )


# ============================================================
# Subscriber Routes (role=subscriber or premium required)
# ============================================================


@api.get(
    "/articles/premium/", response=PaginatedResponse[ArticleBrief], auth=GlobalAuth()
)
def list_premium_articles(
    request: HttpRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
):
    subscriber_required(request.auth)
    qs = (
        Article.objects.filter(
            status=Article.Status.PUBLISHED,
            access=Article.Access.PREMIUM,
        )
        .select_related("author", "category")
        .order_by("-published_at")
    )

    page_obj, next_url, previous_url = _paginate(qs, page, page_size, request)
    results = [_build_article_brief(a) for a in page_obj]
    return PaginatedResponse(
        count=page_obj.paginator.count,
        next=next_url,
        previous=previous_url,
        results=results,
    )


@api.post("/subscriptions/", response=SubscriptionOut, auth=GlobalAuth())
def create_subscription(request: HttpRequest, data: SubscriptionCreate):
    user = subscriber_required(request.auth)
    plan = SubscriptionPlan.objects.filter(id=data.plan_id, is_active=True).first()
    if not plan:
        from ninja.errors import HttpError

        raise HttpError(404, "Plan not found")

    existing = Subscription.objects.filter(
        user=user, status=Subscription.Status.ACTIVE
    ).first()
    if existing:
        from ninja.errors import HttpError

        raise HttpError(400, "User already has an active subscription")

    if plan.interval == "yearly":
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)
    else:
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)

    sub = Subscription.objects.create(
        user=user,
        plan=plan,
        status=Subscription.Status.ACTIVE,
        expires_at=expires_at,
    )

    user.role = User.Role.SUBSCRIBER
    user.save(update_fields=["role"])

    return SubscriptionOut(
        id=str(sub.id),
        plan=SubscriptionPlanOut(
            id=plan.id,
            name=plan.name,
            plan_type=plan.plan_type,
            price=float(plan.price),
            currency=plan.currency,
            interval=plan.interval,
            features=plan.features or [],
            highlighted=plan.highlighted,
            print_included=plan.print_included,
            is_active=plan.is_active,
        ),
        status=sub.status,
        started_at=sub.started_at,
        expires_at=sub.expires_at,
        cancelled_at=sub.cancelled_at,
    )


@api.get("/subscriptions/me/", response=Optional[SubscriptionOut], auth=GlobalAuth())
def get_my_subscription(request: HttpRequest):
    subscriber_required(request.auth)
    sub = (
        Subscription.objects.filter(
            user=request.auth, status=Subscription.Status.ACTIVE
        )
        .select_related("plan")
        .first()
    )
    if not sub:
        return None
    plan = sub.plan
    return SubscriptionOut(
        id=str(sub.id),
        plan=SubscriptionPlanOut(
            id=plan.id,
            name=plan.name,
            plan_type=plan.plan_type,
            price=float(plan.price),
            currency=plan.currency,
            interval=plan.interval,
            features=plan.features or [],
            highlighted=plan.highlighted,
            print_included=plan.print_included,
            is_active=plan.is_active,
        ),
        status=sub.status,
        started_at=sub.started_at,
        expires_at=sub.expires_at,
        cancelled_at=sub.cancelled_at,
    )


# --- Print Orders ---


@api.post("/print/orders/", response=PrintOrderOut, auth=GlobalAuth())
def create_print_order(request: HttpRequest, data: PrintOrderCreate):
    subscriber_required(request.auth)
    edition = Edition.objects.filter(pk=data.edition_id).first()
    if not edition:
        from ninja.errors import HttpError

        raise HttpError(404, "Edition not found")

    is_international = data.shipping_region == "international"
    unit_price = Decimal("14.99") if is_international else Decimal("12.99")
    shipping = Decimal("12.99") if is_international else Decimal("4.99")
    discount = Decimal("0")
    if data.quantity >= 5:
        discount = (unit_price * data.quantity) * Decimal("0.10")
    total = (unit_price * data.quantity) + shipping - discount

    order_id = f"ORD-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    order = PrintOrder.objects.create(
        user=request.auth,
        edition=edition,
        quantity=data.quantity,
        unit_price=unit_price,
        shipping_cost=shipping,
        discount=discount,
        total=total,
        shipping_region=data.shipping_region,
        first_name=data.first_name,
        last_name=data.last_name,
        street=data.street,
        city=data.city,
        state=data.state,
        zip_code=data.zip_code,
        order_id=order_id,
    )
    return PrintOrderOut(
        id=str(order.id),
        order_id=order.order_id,
        edition=_build_edition_brief(edition),
        quantity=order.quantity,
        unit_price=float(order.unit_price),
        shipping_cost=float(order.shipping_cost),
        discount=float(order.discount),
        total=float(order.total),
        shipping_region=order.shipping_region,
        status=order.status,
        first_name=order.first_name,
        last_name=order.last_name,
        street=order.street,
        city=order.city,
        state=order.state,
        zip_code=order.zip_code,
        created_at=order.created_at,
    )


@api.get("/print/orders/", response=List[PrintOrderOut], auth=GlobalAuth())
def list_print_orders(request: HttpRequest):
    subscriber_required(request.auth)
    orders = (
        PrintOrder.objects.filter(
            user=request.auth,
        )
        .select_related("edition")
        .order_by("-created_at")
    )
    return [
        PrintOrderOut(
            id=str(o.id),
            order_id=o.order_id,
            edition=_build_edition_brief(o.edition),
            quantity=o.quantity,
            unit_price=float(o.unit_price),
            shipping_cost=float(o.shipping_cost),
            discount=float(o.discount),
            total=float(o.total),
            shipping_region=o.shipping_region,
            status=o.status,
            first_name=o.first_name,
            last_name=o.last_name,
            street=o.street,
            city=o.city,
            state=o.state,
            zip_code=o.zip_code,
            created_at=o.created_at,
        )
        for o in orders
    ]
