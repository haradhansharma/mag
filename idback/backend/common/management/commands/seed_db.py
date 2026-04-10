"""
Seed command that parses the Astro frontend .ts dummy data files
and populates the Django database.
"""

import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime, parse_date

from common.models import (
    Article,
    Author,
    Category,
    Edition,
    PrintOrder,
)
from users.models import (
    AuthToken,
    EditorialActivity,
    Subscription,
    SubscriptionPlan,
)
from api.auth import create_token_for_user

User = get_user_model()

# Seed data directory — looks for dummy TypeScript files.
# Docker: /app/seed_data (symlink from backend/seed_data -> idfront/src/data/dummy)
# The symlink should be created on the host:
#   ln -s ../../idfront/src/data/dummy backend/seed_data
# DUMMY_DIR = Path(__file__).resolve().parents[2] / "seed_data"
DUMMY_DIR = Path(__file__).resolve().parents[3] / "seed_data"


def _read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


def _find_array_content(text, var_name):
    """Extract the array body for export const <var_name> = [...]"""
    # Non-greedy: capture up to first ];
    pattern = rf"export\s+const\s+{re.escape(var_name)}\s*(?::\s*\w+\[\])?\s*=\s*\[([\s\S]*?)\];"
    m = re.search(pattern, text)
    if not m:
        return ""
    return m.group(1)


def _split_top_level_objects(text):
    """Split text into top-level {}-delimited objects, respecting strings."""
    objects = []
    depth = 0
    start = None
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        # Handle string delimiters
        if ch in ('"', "'", "`"):
            quote = ch
            i += 1
            while i < n:
                c2 = text[i]
                if c2 == "\\":
                    i += 2
                    continue
                if c2 == quote:
                    break
                i += 1
            i += 1
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                objects.append(text[start : i + 1])
                start = None
        i += 1
    return objects


def _extract_string(obj_text, field):
    """Extract a quoted string value for a field."""
    for q in ['"', "'", "`"]:
        pattern = rf"{field}:\s*{q}([^'{q}]*){q}"
        m = re.search(pattern, obj_text)
        if m:
            return m.group(1)
    return ""


def _extract_number(obj_text, field):
    """Extract a numeric value for a field."""
    pattern = rf"{field}:\s*(\d+\.?\d*)"
    m = re.search(pattern, obj_text)
    if m:
        return m.group(1)
    return ""


def _extract_bool(obj_text, field):
    """Extract a boolean value for a field."""
    pattern = rf"{field}:\s*(true|false)"
    m = re.search(pattern, obj_text)
    if m:
        return m.group(1) == "true"
    return ""


def _extract_nested_object(obj_text, field):
    """Extract a nested object block."""
    pattern = rf"{field}:\s*\{{"
    m = re.search(pattern, obj_text)
    if not m:
        return {}
    start = m.start() + len(m.group()) - 1
    depth = 0
    for i in range(start, len(obj_text)):
        ch = obj_text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                block = obj_text[start : i + 1]
                result = {}
                for q in ['"', "'", "`"]:
                    pairs = re.findall(rf"(\w+):\s*{q}([^'{q}]*){q}", block)
                    for k, v in pairs:
                        if k not in result:
                            result[k] = v
                # Also get arrays inside
                arr_pattern = rf"(\w+):\s*\[([^\]]*)\]"
                arr_matches = re.findall(arr_pattern, block)
                for k, v in arr_matches:
                    items = re.findall(r"['\"\`]([^'\"\`]+)['\"\`]", v)
                    if k not in result:
                        result[k] = items
                return result
    return {}


def _extract_string_list(obj_text, field):
    """Extract a simple string array."""
    pattern = rf"{field}:\s*\[([^\]]*)\]"
    m = re.search(pattern, obj_text)
    if not m:
        return []
    items = re.findall(r"['\"\`]([^'\"\`]+)['\"\`]", m.group(1))
    return items


class Command(BaseCommand):
    help = "Seed the database with dummy data from Astro frontend data files"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...\n")

        self._seed_users()
        self._seed_categories()
        self._seed_authors()
        self._seed_editions()
        self._seed_articles()
        self._seed_plans()
        self._seed_editorial_activity()

        self.stdout.write(self.style.SUCCESS("\nDatabase seeded successfully!"))
        self.stdout.write("\nTest accounts:")
        self.stdout.write("  Admin:   admin@meridian.com / admin123")
        self.stdout.write("  Editor:  editor@meridian.com / editor123")
        self.stdout.write("  Writer:  writer@meridian.com / writer123")

    def _seed_users(self):
        self.stdout.write("Creating users...")
        users_data = [
            {
                "username": "admin",
                "email": "admin@meridian.com",
                "password": "admin123",
                "role": User.Role.ADMIN,
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "editor",
                "email": "editor@meridian.com",
                "password": "editor123",
                "role": User.Role.EDITOR,
                "first_name": "Editor",
                "last_name": "User",
            },
            {
                "username": "writer",
                "email": "writer@meridian.com",
                "password": "writer123",
                "role": User.Role.WRITER,
                "first_name": "Writer",
                "last_name": "User",
            },
        ]
        for ud in users_data:
            user, created = User.objects.update_or_create(
                username=ud["username"],
                defaults={
                    "email": ud["email"],
                    "role": ud["role"],
                    "first_name": ud["first_name"],
                    "last_name": ud["last_name"],
                    "is_staff": ud.get("is_staff", False),
                    "is_superuser": ud.get("is_superuser", False),
                },
            )
            user.set_password(ud["password"])
            user.save()
            if created:
                self.stdout.write(f"  Created user: {user.username}")

    def _seed_categories(self):
        self.stdout.write("Creating categories...")
        text = _read_file(DUMMY_DIR / "categories.ts")
        array_text = _find_array_content(text, "categories")
        objects = _split_top_level_objects(array_text)
        for obj in objects:
            cid = _extract_string(obj, "id")
            if not cid:
                continue
            Category.objects.update_or_create(
                id=cid,
                defaults={
                    "name": _extract_string(obj, "name"),
                    "slug": _extract_string(obj, "slug"),
                    "description": _extract_string(obj, "description"),
                    "color": _extract_string(obj, "color"),
                    "access": _extract_string(obj, "access") or "public",
                    "featured": (
                        _extract_bool(obj, "featured")
                        if _extract_bool(obj, "featured") != ""
                        else False
                    ),
                    "article_count": int(_extract_number(obj, "articleCount") or 0),
                },
            )
        self.stdout.write(f"  Created {len(objects)} categories")

    def _seed_authors(self):
        self.stdout.write("Creating authors...")
        text = _read_file(DUMMY_DIR / "authors.ts")
        array_text = _find_array_content(text, "authors")
        objects = _split_top_level_objects(array_text)
        for obj in objects:
            slug = _extract_string(obj, "slug")
            if not slug:
                continue
            socials = _extract_nested_object(obj, "socials")
            Author.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": _extract_string(obj, "name"),
                    "bio": _extract_string(obj, "bio"),
                    "avatar": _extract_string(obj, "avatar"),
                    "role": _extract_string(obj, "role"),
                    "twitter": socials.get("twitter", ""),
                    "linkedin": socials.get("linkedin", ""),
                    "instagram": socials.get("instagram", ""),
                    "website": socials.get("website", ""),
                    "article_count": int(_extract_number(obj, "articleCount") or 0),
                },
            )

        # Link writer/editor users to author profiles
        writer_user = User.objects.get(username="writer")
        editor_user = User.objects.get(username="editor")
        for slug, user in [
            ("sarah-chen", writer_user),
            ("marcus-johnson", editor_user),
        ]:
            author = Author.objects.filter(slug=slug, user__isnull=True).first()
            if author:
                author.user = user
                author.save()

        self.stdout.write(f"  Created {len(objects)} authors")

    def _seed_editions(self):
        self.stdout.write("Creating editions...")
        text = _read_file(DUMMY_DIR / "editions.ts")
        array_text = _find_array_content(text, "editions")
        objects = _split_top_level_objects(array_text)
        for obj in objects:
            slug = _extract_string(obj, "slug")
            number = _extract_number(obj, "number")
            if not slug or not number:
                continue
            pub_str = _extract_string(obj, "publishedAt")
            pub_date = parse_datetime(pub_str) if pub_str else None
            ws = _extract_string(obj, "weekStart")
            we = _extract_string(obj, "weekEnd")
            Edition.objects.update_or_create(
                slug=slug,
                defaults={
                    "number": int(number),
                    "title": _extract_string(obj, "title"),
                    "subtitle": _extract_string(obj, "subtitle"),
                    "cover_image": _extract_string(obj, "coverImage"),
                    "status": _extract_string(obj, "status") or "draft",
                    "published_at": pub_date,
                    "week_start": parse_date(ws) if ws else None,
                    "week_end": parse_date(we) if we else None,
                    "article_count": int(_extract_number(obj, "articleCount") or 0),
                    "print_ready": (
                        _extract_bool(obj, "printReady")
                        if _extract_bool(obj, "printReady") != ""
                        else False
                    ),
                },
            )
        self.stdout.write(f"  Created {len(objects)} editions")

    def _seed_articles(self):
        self.stdout.write("Creating articles...")
        text = _read_file(DUMMY_DIR / "articles.ts")
        array_text = _find_array_content(text, "articles")
        objects = _split_top_level_objects(array_text)

        # Build author slug lookup: 'author-01' -> 'sarah-chen'
        auth_text = _read_file(DUMMY_DIR / "authors.ts")
        auth_array = _find_array_content(auth_text, "authors")
        auth_objs = _split_top_level_objects(auth_array)
        author_id_to_slug = {}
        for ao in auth_objs:
            aid = _extract_string(ao, "id")
            aslug = _extract_string(ao, "slug")
            if aid and aslug:
                author_id_to_slug[aid] = aslug

        author_slug_map = {a.slug: a for a in Author.objects.all()}

        # Build edition slug lookup
        ed_text = _read_file(DUMMY_DIR / "editions.ts")
        ed_array = _find_array_content(ed_text, "editions")
        ed_objs = _split_top_level_objects(ed_array)
        ed_id_to_slug = {}
        for eo in ed_objs:
            eid = _extract_string(eo, "id")
            eslug = _extract_string(eo, "slug")
            if eid and eslug:
                ed_id_to_slug[eid] = eslug

        count = 0
        for obj in objects:
            slug = _extract_string(obj, "slug")
            title = _extract_string(obj, "title")
            if not slug or not title:
                continue

            author_id = _extract_string(obj, "authorId")
            author_slug = author_id_to_slug.get(author_id, "")
            author = author_slug_map.get(author_slug)
            if not author:
                self.stderr.write(f"  WARNING: Author not found for {author_id}")
                continue

            cat_id = _extract_string(obj, "categoryId")
            cat = Category.objects.filter(id=cat_id).first()
            if not cat:
                self.stderr.write(f"  WARNING: Category {cat_id} not found")
                continue

            seo = _extract_nested_object(obj, "seo")
            pub_str = _extract_string(obj, "publishedAt")
            pub_date = parse_datetime(pub_str) if pub_str else None

            feat = _extract_bool(obj, "featured")
            trend = _extract_bool(obj, "trending")
            pin = _extract_bool(obj, "pinned")

            article, created = Article.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "subtitle": _extract_string(obj, "subtitle"),
                    "content": _extract_string(obj, "content"),
                    "excerpt": _extract_string(obj, "excerpt"),
                    "cover_image": _extract_string(obj, "coverImage"),
                    "cover_caption": _extract_string(obj, "coverCaption"),
                    "author": author,
                    "category": cat,
                    "content_type": _extract_string(obj, "contentType") or "article",
                    "access": _extract_string(obj, "access") or "public",
                    "status": Article.Status.PUBLISHED,
                    "seo_title": seo.get("title", ""),
                    "seo_description": seo.get("description", ""),
                    "seo_keywords": seo.get("keywords", []),
                    "published_at": pub_date,
                    "reading_time": int(_extract_number(obj, "readingTime") or 0),
                    "word_count": int(_extract_number(obj, "wordCount") or 0),
                    "featured": feat if feat != "" else False,
                    "trending": trend if trend != "" else False,
                    "pinned": pin if pin != "" else False,
                },
            )
            count += 1

            # Link to edition
            ed_id = _extract_string(obj, "editionId")
            if ed_id:
                ed_slug = ed_id_to_slug.get(ed_id)
                if ed_slug:
                    edition = Edition.objects.filter(slug=ed_slug).first()
                    if edition:
                        edition.articles.add(article)

        self.stdout.write(f"  Created {count} articles")

    def _seed_plans(self):
        self.stdout.write("Creating subscription plans...")
        text = _read_file(DUMMY_DIR / "site-config.ts")
        # subscriptionPlans is a property inside siteConfig, not a standalone export
        m = re.search(r"subscriptionPlans:\s*\[([\s\S]*?)\n  \],", text)
        array_text = m.group(1) if m else ""
        if not array_text:
            self.stderr.write("  Could not parse subscription plans")
            return
        objects = _split_top_level_objects(array_text)
        for obj in objects:
            pid = _extract_string(obj, "id")
            if not pid:
                continue
            features = _extract_string_list(obj, "features")
            highlighted = _extract_bool(obj, "highlighted")
            print_inc = _extract_bool(obj, "printIncluded")
            price = _extract_number(obj, "price")
            SubscriptionPlan.objects.update_or_create(
                id=pid,
                defaults={
                    "name": _extract_string(obj, "name"),
                    "plan_type": _extract_string(obj, "type") or "free",
                    "price": Decimal(price) if price else Decimal("0"),
                    "interval": _extract_string(obj, "interval") or "monthly",
                    "features": features,
                    "highlighted": highlighted if highlighted != "" else False,
                    "print_included": print_inc if print_inc != "" else False,
                },
            )
        self.stdout.write(f"  Created {len(objects)} subscription plans")

    def _seed_editorial_activity(self):
        self.stdout.write("Creating editorial activity...")
        text = _read_file(DUMMY_DIR / "editorial.ts")
        array_text = _find_array_content(text, "editorialActivity")
        if not array_text:
            self.stderr.write("  Could not parse editorial activity")
            return
        objects = _split_top_level_objects(array_text)
        editor_user = User.objects.get(username="editor")
        count = 0
        for obj in objects:
            action_str = _extract_string(obj, "action")
            article_title = _extract_string(obj, "articleTitle")
            if not article_title:
                continue
            article = Article.objects.filter(title=article_title).first()
            if not article:
                # Editorial activity may reference articles not in the main articles list
                # Create a minimal draft article for the activity reference
                first_author = Author.objects.first()
                first_cat = Category.objects.first()
                if first_author and first_cat:
                    article = Article.objects.create(
                        title=article_title,
                        slug=article_title.lower()
                        .replace(" ", "-")
                        .replace(":", "")[:200],
                        author=first_author,
                        category=first_cat,
                        status=Article.Status.DRAFT,
                    )
                else:
                    continue
            ts_str = _extract_string(obj, "timestamp")
            ts = parse_datetime(ts_str) if ts_str else datetime.now(timezone.utc)
            EditorialActivity.objects.create(
                article=article,
                action=action_str or "created",
                performed_by=editor_user,
                details=_extract_string(obj, "details"),
                created_at=ts,
            )
            count += 1
        self.stdout.write(f"  Created {count} editorial activity entries")
