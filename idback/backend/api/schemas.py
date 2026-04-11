from typing import Generic, List, Literal, Optional, TypeVar

from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


T = TypeVar("T")


# ============================================================
# Generic / Shared Schemas
# ============================================================


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[T]


class MessageOut(BaseModel):
    message: str


class SearchFilters(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    access: Optional[str] = None
    featured: Optional[bool] = None
    trending: Optional[bool] = None
    author: Optional[str] = None
    content_type: Optional[str] = None


# ============================================================
# Author Schemas
# ============================================================


class AuthorBrief(BaseModel):
    id: str
    name: str
    slug: str
    avatar: str = ""
    role: str = ""

    class Config:
        from_attributes = True


class AuthorOut(BaseModel):
    id: str
    name: str
    slug: str
    bio: str
    avatar: str = ""
    role: str = ""
    twitter: str = ""
    linkedin: str = ""
    instagram: str = ""
    website: str = ""
    article_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AuthorCreate(BaseModel):
    name: str = Field(max_length=200)
    slug: str = Field(max_length=220)
    bio: str
    role: str = Field(default="", max_length=200)
    twitter: str = Field(default="", max_length=500)
    linkedin: str = Field(default="", max_length=500)
    instagram: str = Field(default="", max_length=500)
    website: str = Field(default="", max_length=500)


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    bio: Optional[str] = None
    role: Optional[str] = Field(default=None, max_length=200)
    twitter: Optional[str] = Field(default=None, max_length=500)
    linkedin: Optional[str] = Field(default=None, max_length=500)
    instagram: Optional[str] = Field(default=None, max_length=500)
    website: Optional[str] = Field(default=None, max_length=500)
    avatar: Optional[str] = None


# ============================================================
# Category Schemas
# ============================================================


class CategoryBrief(BaseModel):
    id: str
    name: str
    slug: str
    color: str
    access: str = "public"

    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    color: str
    access: str = "public"
    icon: str = ""
    featured: bool = False
    article_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    slug: str
    description: str
    color: str = Field(max_length=20)
    access: str = Field(default="public", max_length=10)
    icon: str = Field(default="", max_length=100)
    featured: bool = False


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(default=None, max_length=20)
    access: Optional[str] = Field(default=None, max_length=10)
    icon: Optional[str] = Field(default=None, max_length=100)
    featured: Optional[bool] = None


# ============================================================
# Article Schemas
# ============================================================


class ArticleBrief(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str = ""
    cover_image: str = ""
    author_name: str = ""
    author_slug: str = ""
    category_name: str = ""
    category_slug: str = ""
    published_at: Optional[datetime] = None
    reading_time: int = 0
    content_type: str = "article"
    access: str = "public"
    featured: bool = False
    trending: bool = False
    pinned: bool = False

    class Config:
        from_attributes = True


class ArticleOut(BaseModel):
    id: str
    title: str
    slug: str
    subtitle: str = ""
    content: str = ""
    excerpt: str = ""
    cover_image: str = ""
    cover_caption: str = ""
    author: AuthorBrief
    category: CategoryBrief
    content_type: str = "article"
    access: str = "public"
    status: str = "draft"
    seo_title: str = ""
    seo_description: str = ""
    seo_keywords: list[str] = []
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    reading_time: int = 0
    word_count: int = 0
    featured: bool = False
    trending: bool = False
    pinned: bool = False
    reviewed_by_name: Optional[str] = None
    rejection_reason: str = ""

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    title: str = Field(max_length=500)
    slug: str = Field(max_length=600)
    subtitle: str = Field(default="", max_length=500)
    content: str = ""
    excerpt: str = Field(default="", max_length=500)
    cover_image: str = ""
    cover_caption: str = Field(default="", max_length=500)
    author_id: Optional[str] = None
    category_id: str
    content_type: str = Field(default="article", max_length=20)
    access: str = Field(default="public", max_length=10)
    seo_title: str = Field(default="", max_length=500)
    seo_description: str = Field(default="", max_length=1000)
    seo_keywords: list[str] = []
    reading_time: int = 0
    word_count: int = 0
    featured: bool = False
    trending: bool = False


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=500)
    subtitle: Optional[str] = Field(default=None, max_length=500)
    content: Optional[str] = None
    excerpt: Optional[str] = Field(default=None, max_length=500)
    cover_image: Optional[str] = None
    cover_caption: Optional[str] = Field(default=None, max_length=500)
    category_id: Optional[str] = None
    content_type: Optional[str] = Field(default=None, max_length=20)
    access: Optional[str] = Field(default=None, max_length=10)
    seo_title: Optional[str] = Field(default=None, max_length=500)
    seo_description: Optional[str] = Field(default=None, max_length=1000)
    seo_keywords: Optional[list[str]] = None
    reading_time: Optional[int] = None
    word_count: Optional[int] = None
    featured: Optional[bool] = None
    trending: Optional[bool] = None
    pinned: Optional[bool] = None


class ArticleStatusUpdate(BaseModel):
    status: str = Field(description="One of: approved, rejected, published")
    rejection_reason: str = Field(
        default="", description="Required when status is rejected"
    )


# ============================================================
# Edition Schemas
# ============================================================


class EditionBrief(BaseModel):
    id: str
    number: int
    title: str
    slug: str
    cover_image: str = ""
    status: str = "draft"
    published_at: Optional[datetime] = None
    week_start: Optional[date] = None
    week_end: Optional[date] = None
    article_count: int = 0
    print_ready: bool = False

    class Config:
        from_attributes = True


class EditionOut(BaseModel):
    id: str
    number: int
    title: str
    subtitle: str = ""
    slug: str
    cover_image: str = ""
    status: str = "draft"
    published_at: Optional[datetime] = None
    week_start: Optional[date] = None
    week_end: Optional[date] = None
    featured_article: Optional[ArticleBrief] = None
    print_ready: bool = False
    print_pdf_url: str = ""
    article_count: int = 0
    articles: List[ArticleBrief] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EditionCreate(BaseModel):
    number: int
    title: str = Field(max_length=300)
    subtitle: str = Field(default="", max_length=500)
    slug: str
    week_start: date
    week_end: date
    featured_article_id: Optional[str] = None
    print_ready: bool = False


class EditionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=300)
    subtitle: Optional[str] = Field(default=None, max_length=500)
    week_start: Optional[date] = None
    week_end: Optional[date] = None
    featured_article_id: Optional[str] = None
    print_ready: Optional[bool] = None
    status: Optional[str] = Field(default=None, max_length=20)


# ============================================================
# Subscription Schemas
# ============================================================


class SubscriptionPlanOut(BaseModel):
    id: str
    name: str
    plan_type: str
    price: float
    currency: str = "USD"
    interval: str = "monthly"
    features: list[str] = []
    highlighted: bool = False
    print_included: bool = False
    is_active: bool = True

    class Config:
        from_attributes = True


class SubscriptionOut(BaseModel):
    id: str
    plan: SubscriptionPlanOut
    status: str
    started_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    plan_id: str
    payment_id: Optional[str] = Field(
        default=None, description="External payment reference. Required for paid plans."
    )


class SubscriptionCancel(BaseModel):
    reason: str = Field(default="", max_length=500)


# ============================================================
# Editorial Schemas
# ============================================================


class EditorialQueueItemOut(BaseModel):
    id: str
    title: str
    author_name: str = ""
    author_slug: str = ""
    category_name: str = ""
    category_slug: str = ""
    cover_image: str = ""
    excerpt: str = ""
    status: str = "draft"
    submitted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    reviewed_by_name: Optional[str] = None
    rejection_reason: str = ""
    word_count: int = 0
    reading_time: int = 0

    class Config:
        from_attributes = True


class EditorialActivityOut(BaseModel):
    id: str
    action: str
    article_title: str = ""
    performed_by_name: str = ""
    timestamp: Optional[datetime] = None
    details: str = ""

    class Config:
        from_attributes = True


class EditorialStatsOut(BaseModel):
    total_drafts: int = 0
    in_review: int = 0
    approved: int = 0
    rejected: int = 0
    published_this_week: int = 0
    total_articles: int = 0
    avg_reading_time: int = 0


# ============================================================
# Auth Schemas
# ============================================================


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: str = Field(max_length=254)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class VerifyEmail(BaseModel):
    email: str = Field(max_length=254)
    token: str = Field(max_length=64)


class ResendVerification(BaseModel):
    email: str = Field(max_length=254)


class ForgotPassword(BaseModel):
    email: str = Field(max_length=254)


class ResetPassword(BaseModel):
    email: str = Field(max_length=254)
    token: str = Field(max_length=64)
    new_password: str = Field(min_length=8, max_length=128)


class TokenOut(BaseModel):
    token: str
    user_id: str
    username: str
    role: str
    is_verified: bool = False


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_verified: bool = False
    date_joined: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================
# Print Schemas
# ============================================================


class PrintOrderCreate(BaseModel):
    edition_id: str
    quantity: int = Field(default=1, ge=1, le=100)
    shipping_region: Literal["us", "international"] = Field(default="us")
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    street: str = Field(max_length=300)
    city: str = Field(max_length=100)
    state: str = Field(max_length=100)
    zip_code: str = Field(max_length=20)
    payment_id: Optional[str] = Field(
        default=None, description="External payment reference"
    )


class PrintOrderOut(BaseModel):
    id: str
    order_id: str
    edition: EditionBrief
    quantity: int
    unit_price: float
    shipping_cost: float
    discount: float
    total: float
    shipping_region: str
    status: str
    first_name: str
    last_name: str
    street: str
    city: str
    state: str
    zip_code: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PrintPricingOut(BaseModel):
    unit_price_us: float
    shipping_us: float
    unit_price_international: float
    shipping_international: float
    bulk_discount_threshold: int
    bulk_discount_percent: float
    currency: str = "USD"


# ============================================================
# Homepage Bundle
# ============================================================


class HomepageData(BaseModel):
    featured_articles: List[ArticleBrief] = []
    trending_articles: List[ArticleBrief] = []
    pinned_articles: List[ArticleBrief] = []
    latest_edition: Optional[EditionBrief] = None
    categories: List[CategoryBrief] = []


# ============================================================
# Site Configuration
# ============================================================


class NavLinkOut(BaseModel):
    label: str = ""
    href: str = ""
    access: str = ""


class SocialLinkOut(BaseModel):
    platform: str = ""
    url: str = ""
    label: str = ""


class PaymentGatewayOut(BaseModel):
    id: str = ""
    name: str = ""
    description: str = ""
    icon: str = ""
    payment_link: str = ""
    enabled: bool = True


class SiteConfigOut(BaseModel):
    name: str = "MERIDIAN"
    tagline: str = "Your World, Synthesized"
    description: str = ""
    url: str = ""
    terms_of_service_url: str = "/terms"
    nav_links: List[NavLinkOut] = []
    footer_links: List[NavLinkOut] = []
    social_links: List[SocialLinkOut] = []
    payment_gateways: List[PaymentGatewayOut] = []
    subscription_plans: List[SubscriptionPlanOut] = []
    print_pricing: Optional[PrintPricingOut] = None
