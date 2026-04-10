# from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
import uuid


class SiteConfig(Site):
    """Custom site model extending Django's built-in Site."""

    # Example additional fields
    site_title = models.CharField(max_length=255, blank=True, default="")
    support_email = models.EmailField(blank=True, null=True)
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Custom Site"
        verbose_name_plural = "Custom Sites"

    def __str__(self):
        return f"{self.domain} ({self.site_title or 'No title'})"


class SiteSettings(models.Model):
    """Site-specific settings attached to the Django sites framework."""

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="settings")
    homepage_description = models.TextField(blank=True)
    allow_registration = models.BooleanField(default=True)
    max_users = models.PositiveIntegerField(default=0, help_text="0 means unlimited")

    # --- Configuration stored as JSON (all configurable from admin) ---
    # Pricing configuration
    pricing_config = models.JSONField(
        default=dict,
        help_text='{"subscription_plans": {"currency": "USD"}, "print": {"us": {"unit": "12.99", "shipping": "4.99"}, "international": {"unit": "14.99", "shipping": "12.99"}, "bulk_threshold": 5, "bulk_discount_percent": "10.0"}}',
    )

    # Rate limiting configuration
    rate_limit_config = models.JSONField(
        default=dict,
        help_text='{"login": {"max_attempts": 5, "window_seconds": 60}, "register": {"max_attempts": 3, "window_seconds": 3600}, "api": {"max_requests": 100, "window_seconds": 60}, "otp": {"max_attempts": 5, "window_seconds": 300}}',
    )

    # Security configuration
    security_config = models.JSONField(
        default=dict,
        help_text='{"admin_allowed_ips": [], "allowed_countries": [], "token_lifetime_days": 7, "password_min_length": 8}',
    )

    # Content moderation configuration
    content_config = models.JSONField(
        default=dict,
        help_text='{"require_editor_approval": true, "auto_moderate": false, "banned_words": [], "max_article_word_count": 10000}',
    )

    # Feature flags
    feature_flags = models.JSONField(
        default=dict,
        help_text='{"subscriptions_enabled": true, "print_orders_enabled": true, "comments_enabled": false, "social_auth_enabled": false, "otp_via_sms_enabled": false}',
    )

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Settings for {self.site.domain}"

    def get_pricing(self):
        """Get pricing config with defaults merged in."""
        defaults = {
            "subscription_plans": {"currency": "USD"},
            "print": {
                "us": {"unit": "12.99", "shipping": "4.99"},
                "international": {"unit": "14.99", "shipping": "12.99"},
                "bulk_threshold": 5,
                "bulk_discount_percent": "10.0",
            },
        }
        config = {**defaults}
        config.update(self.pricing_config or {})
        return config

    def get_rate_limits(self):
        """Get rate limit config with defaults merged in."""
        defaults = {
            "login": {"max_attempts": 5, "window_seconds": 60},
            "register": {"max_attempts": 3, "window_seconds": 3600},
            "api": {"max_requests": 100, "window_seconds": 60},
            "otp": {"max_attempts": 5, "window_seconds": 300},
        }
        config = {**defaults}
        config.update(self.rate_limit_config or {})
        return config

    def get_security(self):
        """Get security config with defaults merged in."""
        defaults = {
            "admin_allowed_ips": [],
            "allowed_countries": [],
            "token_lifetime_days": 7,
            "password_min_length": 8,
        }
        config = {**defaults}
        config.update(self.security_config or {})
        return config

    def get_content_config(self):
        """Get content moderation config with defaults merged in."""
        defaults = {
            "require_editor_approval": True,
            "auto_moderate": False,
            "banned_words": [],
            "max_article_word_count": 10000,
        }
        config = {**defaults}
        config.update(self.content_config or {})
        return config

    def get_feature_flags(self):
        """Get feature flags with defaults merged in."""
        defaults = {
            "subscriptions_enabled": True,
            "print_orders_enabled": True,
            "comments_enabled": False,
            "social_auth_enabled": False,
            "otp_via_sms_enabled": False,
        }
        config = {**defaults}
        config.update(self.feature_flags or {})
        return config


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
        "users.User",
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
    submitted_at = models.DateTimeField(null=True, blank=True)
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
        "users.User",
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
    payment_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="External payment reference",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "print_orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.order_id}"
