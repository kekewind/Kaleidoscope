import time

import MyUtils
from retrying import retry


@retry(retry_on_exception=MyUtils.retry)
def main():
    raise MyUtils.MyError


if __name__ == '__main__':
    main()
