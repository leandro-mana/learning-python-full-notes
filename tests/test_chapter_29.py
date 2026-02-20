"""Tests for Chapter 29: Date, Time, and Scheduling."""

import calendar
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


class TestDatetimeFundamentals:
    """Test datetime basics."""

    def test_date_creation(self) -> None:
        """date objects represent calendar dates."""
        d = date(2025, 6, 15)
        assert d.year == 2025
        assert d.month == 6
        assert d.day == 15

    def test_time_creation(self) -> None:
        """time objects represent times of day."""
        t = time(14, 30, 45)
        assert t.hour == 14
        assert t.minute == 30
        assert t.second == 45

    def test_datetime_combines_date_and_time(self) -> None:
        """datetime combines date and time."""
        dt = datetime(2025, 6, 15, 14, 30)
        assert dt.date() == date(2025, 6, 15)
        assert dt.time() == time(14, 30)

    def test_timedelta_arithmetic(self) -> None:
        """timedelta supports date arithmetic."""
        d1 = date(2025, 1, 1)
        d2 = d1 + timedelta(days=30)
        assert d2 == date(2025, 1, 31)

        diff = date(2025, 3, 1) - date(2025, 1, 1)
        assert diff.days == 59

    def test_timedelta_components(self) -> None:
        """timedelta stores days, seconds, and microseconds."""
        td = timedelta(hours=25, minutes=30)
        assert td.days == 1
        assert td.seconds == 5400  # 1.5 hours in seconds

    def test_date_comparison(self) -> None:
        """Dates support comparison operators."""
        assert date(2025, 6, 1) < date(2025, 7, 1)
        assert date(2025, 12, 31) > date(2025, 1, 1)


class TestTimezones:
    """Test timezone handling."""

    def test_utc_timezone(self) -> None:
        """timezone.utc is the UTC timezone."""
        dt = datetime(2025, 6, 15, 12, 0, tzinfo=timezone.utc)
        assert dt.tzinfo == timezone.utc
        assert dt.tzname() == "UTC"

    def test_zoneinfo_timezone(self) -> None:
        """ZoneInfo provides IANA timezone support."""
        tz = ZoneInfo("America/New_York")
        dt = datetime(2025, 6, 15, 12, 0, tzinfo=tz)
        assert dt.tzinfo is not None
        assert "America/New_York" in str(dt.tzinfo)

    def test_timezone_conversion(self) -> None:
        """astimezone converts between timezones."""
        utc = datetime(2025, 6, 15, 12, 0, tzinfo=timezone.utc)
        eastern = utc.astimezone(ZoneInfo("America/New_York"))
        assert eastern.hour == 8  # UTC-4 in June (EDT)
        assert eastern.date() == utc.date()

    def test_naive_vs_aware(self) -> None:
        """Naive datetimes have no timezone info."""
        naive = datetime(2025, 6, 15, 12, 0)
        aware = datetime(2025, 6, 15, 12, 0, tzinfo=timezone.utc)
        assert naive.tzinfo is None
        assert aware.tzinfo is not None


class TestFormattingAndCalendar:
    """Test date formatting and calendar utilities."""

    def test_strftime_formatting(self) -> None:
        """strftime formats datetime to string."""
        dt = datetime(2025, 6, 15, 14, 30)
        assert dt.strftime("%Y-%m-%d") == "2025-06-15"
        assert dt.strftime("%H:%M") == "14:30"
        assert dt.strftime("%A") == "Sunday"

    def test_strptime_parsing(self) -> None:
        """strptime parses string to datetime."""
        dt = datetime.strptime("2025-06-15", "%Y-%m-%d")
        assert dt.year == 2025
        assert dt.month == 6
        assert dt.day == 15

    def test_isoformat(self) -> None:
        """isoformat produces ISO 8601 strings."""
        dt = datetime(2025, 6, 15, 14, 30, tzinfo=timezone.utc)
        iso = dt.isoformat()
        assert "2025-06-15" in iso
        assert "14:30" in iso

    def test_fromisoformat(self) -> None:
        """fromisoformat parses ISO 8601 strings."""
        dt = datetime.fromisoformat("2025-06-15T14:30:00")
        assert dt == datetime(2025, 6, 15, 14, 30)

    def test_calendar_isleap(self) -> None:
        """calendar.isleap checks for leap years."""
        assert calendar.isleap(2024) is True
        assert calendar.isleap(2025) is False
        assert calendar.isleap(2000) is True
        assert calendar.isleap(1900) is False

    def test_calendar_monthrange(self) -> None:
        """calendar.monthrange returns weekday and days in month."""
        weekday, days = calendar.monthrange(2025, 2)
        assert days == 28  # Not a leap year
        _, days_leap = calendar.monthrange(2024, 2)
        assert days_leap == 29
