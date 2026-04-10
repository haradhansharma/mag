import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        VISITOR = "visitor", "Visitor"
        SUBSCRIBER = "subscriber", "Subscriber"
        WRITER = "writer", "Writer"
        EDITOR = "editor", "Editor"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VISITOR)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.username} ({self.role})"


class Category(models.Model):
    class Color(models.TextChoices):
        BLUE = "blue", "Blue"
        PURPLE = "purple", "Purple"
        GREEN = "green", "Green"
        ROSE = "rose", "Rose"
        AMBER = "amber", "Amber"
        TEAL = "teal", "Teal"
        INDIGO = "indigo", "Indigo"
        ORANGE = "orange", "Orange"
        CYAN = "cyan", "Cyan"
        PINK = "pink", "Pink"
        EMERALD = "emerald", "Emerald"

    class Access(models.TextChoices):
        PUBLIC = "public", "Public"
        PREMIUM = "premium", "Premium"

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField()
    color = models.CharField(max_length=20, choices=Color.choices)
    access = models.CharField(
        max_length=10, choices=Access.choices, default=Access.PUBLIC
    )
    icon = models.CharField(max_length=100, blank=True, default="")
    featured = models.BooleanField(default=False)
    article_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="author_profile",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    bio = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", blank=True, default="")
    role = models.CharField(max_length=200, default="")
    twitter = models.URLField(blank=True, default="")
    linkedin = models.URLField(blank=True, default="")
    instagram = models.URLField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    article_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "authors"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Edition(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "published", "Published"
        SCHEDULED = "scheduled", "Scheduled"
        DRAFT = "draft", "Draft"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=500, blank=True, default="")
    slug = models.SlugField(unique=True, max_length=320)
    cover_image = models.ImageField(upload_to="editions/", blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    published_at = models.DateTimeField(null=True, blank=True)
    week_start = models.DateField()
    week_end = models.DateField()
    featured_article = models.ForeignKey(
        "Article",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="featured_in",
    )
    print_ready = models.BooleanField(default=False)
    print_pdf_url = models.FileField(
        upload_to="editions/pdfs/",
        blank=True,
        default="",
    )
    article_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "editions"
        ordering = ["-number"]

    def __str__(self):
        return f"Edition #{self.number}: {self.title}"


class Article(models.Model):
    class ContentType(models.TextChoices):
        ARTICLE = "article", "Article"
        FEATURE = "feature", "Feature"
        OPINION = "opinion", "Opinion"
        BRIEF = "brief", "Brief"
        EXPLAINER = "explainer", "Explainer"
        INTERVIEW = "interview", "Interview"

    class Access(models.TextChoices):
        PUBLIC = "public", "Public"
        PREMIUM = "premium", "Premium"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_REVIEW = "in_review", "In Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PUBLISHED = "published", "Published"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=600)
    subtitle = models.CharField(max_length=500, blank=True, default="")
    content = models.TextField(default="")
    excerpt = models.CharField(max_length=500, default="")
    cover_image = models.ImageField(upload_to="articles/", blank=True, default="")
    cover_caption = models.CharField(max_length=500, blank=True, default="")
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    editions = models.ManyToManyField(
        Edition,
        blank=True,
        related_name="articles",
    )
    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
        default=ContentType.ARTICLE,
    )
    access = models.CharField(
        max_length=10,
        choices=Access.choices,
        default=Access.PUBLIC,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    seo_title = models.CharField(max_length=500, blank=True, default="")
    seo_description = models.CharField(max_length=1000, blank=True, default="")
    seo_keywords = models.JSONField(blank=True, default=list)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reading_time = models.PositiveIntegerField(default=0)
    word_count = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_articles",
    )
    rejection_reason = models.TextField(blank=True, default="")

    class Meta:
        db_table = "articles"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["slug"], name="idx_articles_slug"),
            models.Index(fields=["category"], name="idx_articles_category"),
            models.Index(fields=["author"], name="idx_articles_author"),
            models.Index(fields=["published_at"], name="idx_articles_published"),
            models.Index(fields=["status"], name="idx_articles_status"),
            models.Index(fields=["access"], name="idx_articles_access"),
        ]

    def __str__(self):
        return self.title


class SubscriptionPlan(models.Model):
    class PlanType(models.TextChoices):
        FREE = "free", "Free"
        PREMIUM = "premium", "Premium"
        PRINT = "print", "Print"
        PREMIUM_PRINT = "premium_print", "Premium Print"

    class Interval(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PlanType.choices)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    interval = models.CharField(max_length=10, choices=Interval.choices)
    features = models.JSONField(default=list)
    highlighted = models.BooleanField(default=False)
    print_included = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscription_plans"
        ordering = ["price"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"
        PAST_DUE = "past_due", "Past Due"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "subscriptions"
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class EditorialActivity(models.Model):
    class Action(models.TextChoices):
        CREATED = "created", "Created"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        EDITED = "edited", "Edited"
        PUBLISHED = "published", "Published"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="editorial_actions",
    )
    details = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "editorial_activities"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.article.title}"


class PrintOrder(models.Model):
    class ShippingRegion(models.TextChoices):
        US = "us", "US"
        INTERNATIONAL = "international", "International"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_region = models.CharField(
        max_length=20,
        choices=ShippingRegion.choices,
        default=ShippingRegion.US,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    street = models.CharField(max_length=300, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=20, default="")
    order_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "print_orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_id}"


class AuthToken(models.Model):
    """Simple token-based authentication model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auth_tokens")
    key = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_tokens"

    def __str__(self):
        return f"Token for {self.user.username}"
