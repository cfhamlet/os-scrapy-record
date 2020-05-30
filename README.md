# os-scrapy-record

[![Build Status](https://www.travis-ci.org/cfhamlet/os-scrapy-record.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-scrapy-record)
[![codecov](https://codecov.io/gh/cfhamlet/os-scrapy-record/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-scrapy-record)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-scrapy-record.svg)](https://pypi.python.org/pypi/os-scrapy-record)
[![PyPI](https://img.shields.io/pypi/v/os-scrapy-record.svg)](https://pypi.python.org/pypi/os-scrapy-record)

This project provide extensions to process Response/Failure, generate standard Item.

## Install

```
pip install os-scrapy-record
```

You can run example spider directly in the project root path

```
scrapy crawl example
```

## APIs

* ``os_scrapy_record.ResponseCallback``

    - the ``callback`` method of this extension will replace the default ``Request.callback``, process Response and generate FetchRecord
    - the ``callback`` method will not work when the request already set callback function
    - the ``callback`` method will override the ``parse`` method of spider
    - enable extension in the project settings.py file:

    ```
    EXTENSIONS = {
        "os_scrapy_record.ResponseCallback": 1,
    }
    ```

* ``os_scrapy_record.ResponseErrback``

    - the ``errback`` method of this extension will replace the default ``Request.errback``, process Failure and generate FetchRecord
    - the ``errback`` method will not work when the request already set errback function
    - enable extension in the project settings.py file:

    ```
    EXTENSIONS = {
        "os_scrapy_record.ResponseErrback": 1,
    }
    ```

* ``os_scrapy_record.FetchRecord``

    This class is subclass of [Item](https://docs.scrapy.org/en/latest/topics/items.html#module-scrapy.item)

    the mumbers of this class are:

    - request: ``os_scrapy_record.items.RequestItem``, members: url, method, headers, body 
    - meta: ``dict``, request.meta, it is better to use lower case and '_' as separator as key
    - response: ``os_scrapy_record.items.ResponseItem``，members: headers, body, status, ip_address(Scrapy 2.1.0+), failure

* ``os_scrapy_record.fetch_status.FetchStatus``

    A mumber of ResponseItem, include HTTP, DNS, Network and user defined status. It is a two-tuple object: group and code. e.g, HTTP:200, DNS:-2, SERVER:111, RULE:16

## Unit Tests

```
sh scripts/test.sh
```

## License

MIT licensed.
