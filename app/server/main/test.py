import coverage
import pytest

cov = coverage.Coverage()
cov.start()

pytest.main(["test"])

cov.stop()
cov.save()
