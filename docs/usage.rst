=====
Usage
=====

``lazy_qa`` is designed as a reusable QA automation utility package.

Basic import:

.. code-block:: python

    import lazy_qa

Practical examples:

.. code-block:: python

    from lazy_qa import generate_unique_id, load_json_as_dict, zip_payload

    test_id = generate_unique_id(10)
    request_body = load_json_as_dict("payload.json")
    compressed_body = zip_payload(str(request_body))
