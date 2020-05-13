# os-scrapy-record

This project provide extensions to process Response/Failure, generate standard Item.

## Install

```
pip install os-scrapy-record
```

You can run example spider directly in the project root path.

```
scrapy crawl example
```

## APIs

* ``scrapy_record.ResponseCallback``

    - the ``callback`` method of this extension will replace the default ``Request.callback``, process Response and generate FetchRecord
    - the ``callback`` method will not work when the request already set callback function
    - the ``callback`` method will override the ``parse`` method of spider
    - enable extension in the project settings.py file:

    ```
    EXTENSIONS = {
        "scrapy_record.ResponseCallback": 1,
    }
    ```

* ``scrapy_record.ResponseErrback``

    - the ``errback`` method of this extension will replace the default ``Request.errback``, process Failure and generate FetchRecord
    - the ``errback`` method will not work when the request already set errback function
    - enable extension in the project settings.py file:

    ```
    EXTENSIONS = {
        "scrapy_record.ResponseErrback": 1,
    }
    ```

* ``scrapy_record.FetchRecord``

    This class is subclass of [Item](https://docs.scrapy.org/en/latest/topics/items.html#module-scrapy.item)

    the mumbers of this class are:

    - request: ``scrapy_record.items.RequestItem``, members: url，method，headers 
    - meta: ``dict``, request.meta
    - response: ``scrapy_record.items.ResponseItem``，members: headers，body，status，ip_address(Scrapy 2.1.0+), failure

* ``scrapy_record.fetch_status.FetchStatus``

    A mumber of ResponseItem, include HTTP, DNS, Network and user defined status. It is a two-tuple object: group and code. e.g, HTTP:200, DNS:-2, SERVER:111, RULE:16

## Unit Tests

```
tox
```

## License

MIT licensed.
