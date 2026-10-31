import pytest
from course_registration import can_register, waitlist_position, late_fee


# ================= CAN REGISTER TESTS =================

def test_unknown_student_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("invalid", 10, 3, True)


def test_invalid_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_prerequisites_missing():
    assert can_register("regular", 10, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("probation", 15, 2, True) == "credit limit exceeded"


def test_successful_registration():
    assert can_register("regular", 20, 4, True) == "registered"


# ================= WAITLIST TESTS =================

def test_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)


def test_seat_available():
    assert waitlist_position(5, 10, 0) == 0


def test_waitlist_full():
    assert waitlist_position(10, 10, 10) == -1


def test_normal_waitlist_position():
    assert waitlist_position(10, 10, 3) == 4


# ================= LATE FEE TESTS =================

def test_no_late_fee():
    assert late_fee(0, 10, False) == 0


def test_negative_late_days():
    assert late_fee(-2, 10, False) == 0


def test_fee_waiver():
    assert late_fee(5, 10, True) == 0


def test_late_fee_within_seven_days():
    assert late_fee(7, 10, False) == 500


def test_late_fee_after_seven_days():
    assert late_fee(8, 10, False) == 600


def test_additional_fee_for_high_credits():
    assert late_fee(8, 21, False) == 850


def test_maximum_fee_cap():
    assert late_fee(30, 21, False) == 2000
