from datetime import datetime
from typing import Any, Dict, Optional, Tuple, Type, TypeVar
from dateutil.relativedelta import relativedelta

import regex
from regex import Regex
import enum

T = TypeVar("T", bound="Artifact")


class Artifact:
    def __init__(self) -> None:
        self.mstart = 0
        self.mend = 0
        self._attrs = ["mstart", "mend"]

    def update_span(self: T, *args: "Artifact") -> T:
        self.mstart = args[0].mstart
        self.mend = args[-1].mend
        return self

    def __len__(self) -> int:
        return self.mend - self.mstart

    def __bool__(self) -> bool:
        return True

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return "{}[{}-{}]{{{}}}".format(
            self.__class__.__name__, self.mstart, self.mend, str(self)
        )

    def nb_str(self) -> str:
        """Return a string representation without the bounds information."""
        return "{}[]{{{}}}".format(self.__class__.__name__, str(self))

    def __eq__(self, other: Any) -> bool:
        if type(other) != type(self):
            return False
        else:
            return all(getattr(self, a) == getattr(other, a) for a in self._attrs)

    def __hash__(self) -> int:
        return hash(tuple(getattr(self, a) for a in self._attrs))

    def _hasOnly(self, *args: str) -> bool:
        """check that all attributes set to True are set (i.e. not None) and
        all set to False are not set (i.e. None)

        """
        return all(
            getattr(self, a) is not None if a in args else getattr(self, a) is None
            for a in self._attrs
        )

    def _hasAtLeast(self, *args: str) -> bool:
        """check that all attributes set to True are set (i.e. not None) and
        all set to False are not set (i.e. None)

        """
        return all(getattr(self, a) is not None for a in args)


class RegexMatch(Artifact):
    def __init__(self, id: int, m: Regex) -> None:
        super().__init__()
        self._attrs = ["mstart", "mend", "id"]
        self.key = "R{}".format(id)
        self.id = id
        self.match = m
        self.mstart = m.span(self.key)[0]
        self.mend = m.span(self.key)[1]
        self._text = m.group(self.key)

    def __str__(self) -> str:
        return "{}:{}".format(self.id, self._text)


_pod_hours = {
    "earlymorning": {
        "offset": (4, 7),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "morning": {
        "offset": (6, 9),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "forenoon": {
        "offset": (9, 12),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "noon": {
        "offset": (11, 13),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "afternoon": {
        "offset": (12, 17),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "evening": {
        "offset": (17, 20),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "lateevening": {
        "offset": (18, 21),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "night": {
        "offset": (19, 22),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (-1, -1),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (1, 1),
        },
    },
    "first": {
        "offset": (0, 0),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (0, 0),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (0, 0),
        },
    },
    "last": {
        "offset": (23, 23),
        "early": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (0, 0),
        },
        "late": {
            "early": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "late": {"offset": (0, 0), "very": {"offset": (0, 0)}},
            "very": {"offset": (0, 0)},
            "offset": (0, 0),
        },
    },
}


def _mk_pod_hours() -> Dict[str, Tuple[int, int]]:
    def _add_ts(t1: Tuple[int, int], t2: Tuple[int, int]) -> Tuple[int, int]:
        return (t1[0] + t2[0], t1[1] + t2[1])

    def _mk(
        pod: str, pod_data: Dict[str, Any], t: Tuple[int, int]
    ) -> Dict[str, Tuple[int, int]]:
        r = {pod: _add_ts(t, pod_data["offset"])}
        for k, v in pod_data.items():
            if k == "offset":
                continue
            r.update(_mk(k + pod, v, r[pod]))
        return r

    res = {}
    for k, v in _pod_hours.items():
        if k == "offset":
            continue
        res.update(_mk(k, v, (0, 0)))
    return res


pod_hours = _mk_pod_hours()


_TIME_REGEX = regex.compile(
    r"(\d{4}|X)-(\d{2}|X)-(\d{2}|X) (\d{2}|X):(\d{2}|X) \((\d|X)\/(\w+)\)"
)


class Time(Artifact):
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        DOW: Optional[int] = None,
        POD: Optional[str] = None,
        period: Optional[str] = None,
    ) -> None:
        super().__init__()
        self._attrs = ["year", "month", "day", "hour", "minute", "DOW", "POD", "period"]
        # Might add some validation here, did not to avoid the overhead
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.DOW = DOW
        self.POD = POD
        self.period = period

    # -----------------------------------------------------------------------------
    # Make sure to not accidentially test bool(x) as False when x==0, but you meant
    # x==None
    # -----------------------------------------------------------------------------
    @property
    def isDOY(self) -> bool:
        """isDayOfYear <=> a dd.mm but not year
        """
        return self._hasOnly("month", "day")

    @property
    def isDOM(self) -> bool:
        """isDayOfMonth <=> a dd but no month
        """
        return self._hasOnly("day")

    @property
    def isDOW(self) -> bool:
        """isDayOfWeek <=> DOW is the 0=Monday index; fragile test, as the DOW
        could be accompanied by e.g. a full date etc.; in practice,
        however, the production rules do not do that.

        """
        return self._hasOnly("DOW")

    @property
    def isMonth(self) -> bool:
        return self._hasOnly("month")

    @property
    def isPOD(self) -> bool:
        """isPartOfDay <=> morning, etc.; fragile, tests only that there is a
        POD and neither a full date nor a full time
        """
        return self._hasOnly("POD")

    @property
    def isHour(self) -> bool:
        """only has an hour"""
        return self._hasOnly("hour")

    @property
    def isTOD(self) -> bool:
        """isTimeOfDay - only a time, not date"""
        return self._hasOnly("hour") or self._hasOnly("hour", "minute") or self._hasOnly("hour", "period") or self._hasOnly("hour", "minute", "period")

    @property
    def isDate(self) -> bool:
        """isDate - only a date, not time"""
        return self._hasOnly("year", "month", "day")

    @property
    def isDateTime(self) -> bool:
        """a date and a time"""
        return self._hasOnly("year", "month", "day", "hour") or self._hasOnly(
            "year", "month", "day", "hour", "minute"
        )

    @property
    def isYear(self) -> bool:
        """just a year"""
        return self._hasOnly("year")

    @property
    def hasDate(self) -> bool:
        """at least a date"""
        return self._hasAtLeast("year", "month", "day")

    @property
    def hasDOY(self) -> bool:
        """at least a day of year"""
        return self._hasAtLeast("month", "day")

    @property
    def hasDOW(self) -> bool:
        """at least a day of week"""
        return self._hasAtLeast("DOW")

    @property
    def hasTime(self) -> bool:
        """at least a time to the hour"""
        return self._hasAtLeast("hour") or self._hasOnly("hour", "period")

    @property
    def hasPeriod(self) -> bool:
        """at least a period"""
        return self._hasAtLeast("period")

    @property
    def hasPOD(self) -> bool:
        """at least a part of day"""
        return self._hasAtLeast("POD")

    def __str__(self) -> str:
        return "{}-{}-{} {}:{} ({}/{})".format(
            "{:04d}".format(self.year) if self.year is not None else "X",
            "{:02d}".format(self.month) if self.month is not None else "X",
            "{:02d}".format(self.day) if self.day is not None else "X",
            "{:02d}".format(self.hour) if self.hour is not None else "X",
            "{:02d}".format(self.minute) if self.minute is not None else "X",
            "{:d}".format(self.DOW) if self.DOW is not None else "X",
            "{}".format(self.POD) if self.POD is not None else "X",
        )

    @classmethod
    def from_str(cls: Type["Time"], text: str) -> "Time":
        match = _TIME_REGEX.match(text)
        if not match:
            raise ValueError("Invalid format")
        else:

            def parse_opt_int(x: str) -> Optional[int]:
                return None if x == "X" else int(x)

            pod = match.group(7)
            return cls(
                year=parse_opt_int(match.group(1)),
                month=parse_opt_int(match.group(2)),
                day=parse_opt_int(match.group(3)),
                hour=parse_opt_int(match.group(4)),
                minute=parse_opt_int(match.group(5)),
                DOW=parse_opt_int(match.group(6)),
                POD=None if pod == "X" else pod,
            )

    @property
    def start(self) -> "Time":
        if self.hour is None and self.hasPOD:
            hour = pod_hours[self.POD][0]  # type: ignore
        else:
            hour = self.hour or 0
        return Time(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=hour,
            minute=self.minute or 0,
            period=self.period,
        )

    @property
    def end(self) -> "Time":
        if self.hour is None and self.hasPOD:
            hour = pod_hours[self.POD][1]  # type: ignore
        else:
            hour = self.hour if self.hour is not None else 23
        return Time(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=hour,
            minute=self.minute if self.minute is not None else 59,
            period=self.period,
        )

    @property
    def dt(self) -> datetime:
        # Use the start time, in case we have a POD specification
        t = self.start
        if t.year is None or t.month is None or t.day is None:
            raise ValueError(
                "cannot convert underspecified Time into datetime"
                ", missing at least one of year, month or day"
            )
        return datetime(t.year, t.month, t.day, t.hour or 0, t.minute or 0)


class Interval(Artifact):
    def __init__(
        self, t_from: Optional[Time] = None, t_to: Optional[Time] = None
    ) -> None:
        super().__init__()
        self._attrs = ["t_from", "t_to"]
        self.t_from = t_from
        self.t_to = t_to

    @property
    def isTimeInterval(self) -> bool:
        if self.t_from is None or self.t_to is None:
            return False
        else:
            return self.t_from.isTOD and self.t_to.isTOD

    @property
    def isDateInterval(self) -> bool:
        if self.t_from is None or self.t_to is None:
            return False
        return self.t_from.isDate and self.t_to.isDate

    def __str__(self) -> str:
        return "{} - {}".format(str(self.t_from), str(self.t_to))

    @classmethod
    def from_str(cls: Type["Interval"], text: str) -> "Interval":
        bounds = text.split(" - ")
        if len(bounds) != 2:
            raise ValueError("Invalid format")

        t_from = None if bounds[0] == "None" else Time.from_str(bounds[0])
        t_to = None if bounds[1] == "None" else Time.from_str(bounds[1])
        return cls(t_from=t_from, t_to=t_to)

    @property
    def start(self) -> Optional[Time]:
        if self.t_from is not None:
            return self.t_from.start
        else:
            return None

    @property
    def end(self) -> Optional[Time]:
        if self.t_to is not None:
            return self.t_to.end
        else:
            return None


@enum.unique
class DurationUnit(enum.Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    NIGHTS = "nights"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"


class Duration(Artifact):
    def __init__(self, value: int, unit: DurationUnit):
        """Create a Duration using value and unit.

        Typical values for unit are:

        minute, hour, day, night, week, month, year
        """
        super().__init__()
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return "{} {}".format(self.value, self.unit.value)

    @classmethod
    def from_str(cls: Type["Duration"], text: str) -> "Duration":
        value, unit = text.split()
        return Duration(int(value), DurationUnit(unit))

    def time(self, ts: datetime) -> Time:
        if self.unit == DurationUnit.MINUTES:
            dm = ts + relativedelta(minutes=+self.value)
            return Time(year=dm.year, month=dm.month, day=dm.day, hour=dm.hour, minute=dm.minute)
        if self.unit == DurationUnit.HOURS:
            dm = ts + relativedelta(hours=+self.value)
            return Time(year=dm.year, month=dm.month, day=dm.day, hour=dm.hour, minute=dm.minute)
        if self.unit == DurationUnit.DAYS:
            dm = ts + relativedelta(days=+self.value)
        if self.unit == DurationUnit.WEEKS:
            dm = ts + relativedelta(days=+self.value*7)
        if self.unit == DurationUnit.MONTHS:
            dm = ts + relativedelta(months=+self.value)
        if self.unit == DurationUnit.YEARS:
            dm = ts + relativedelta(years=+self.value)

        return Time(year=dm.year, month=dm.month, day=dm.day)


@enum.unique
class RecurringFrequency(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Recurring(Artifact):
    def __init__(
        self,
        frequency: Optional[RecurringFrequency] = None,
        interval: Optional[int] = None,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
    ):
        super().__init__()
        self._attrs = ['start_time', 'end_time', 'frequency', 'interval']
        self.start_time = start_time
        self.end_time = end_time
        self.frequency = frequency
        self.interval = interval

    def __str__(self) -> str:
        return "{} {} {} {}".format(self.frequency, self.interval, self.start_time, self.end_time)

    @property
    def isRecurring(self) -> bool:
        if self.frequency and self.interval is None:
            return False
        else:
            return True

    @property
    def isRecurringDOW(self) -> bool:
        if not self.start_time.DOW:
            return False
        else:
            return True

    @property
    def isRecurringTime(self) -> bool:
        if not self.start_time.hasTime:
            return False
        else:
            return True


class RecurringArray(Artifact):
    def __init__(self,
                 rec_1: Optional[Recurring] = None,
                 rec_2: Optional[Recurring] = None,
                 rec_3: Optional[Recurring] = None,
                 rec_4: Optional[Recurring] = None,
                 rec_5: Optional[Recurring] = None,
                 ):
        super().__init__()
        self._attrs = ['rec_1', 'rec_2', 'rec_3', 'rec_4', 'rec_5']
        self.rec_1 = rec_1
        self.rec_2 = rec_2
        self.rec_3 = rec_3
        self.rec_4 = rec_4
        self.rec_5 = rec_5

    def __str__(self) -> str:
        return "\n Recurring instance: {} \n Recurring instance: {} \n Recurring instance: {} \n Recurring instance: {} \n Recurring instance: {}".format(self.rec_1, self.rec_2, self.rec_3, self.rec_4, self.rec_5)

    @property
    def to_list(self) -> list:
        array = [self.rec_1, self.rec_2, self.rec_3, self.rec_4, self.rec_5]
        array = [i for i in array if i != None]
        return array
