import tfat.pipeline as pipe


def test_pipeline_task():
    """ Given I have a series of numbers
        When I apply a series of tasks to them
        Then I should see the result of those tasks,
        and not the original numbers
    """
    n = 10

    global t
    t = []

    def collect_results(data, **kwargs):
        global t
        t.append(data)
        return data

    def double(data, **kwargs):
        return data * 2

    def inc(data, **kwargs):
        return data + 1

    worker = pipe.Pipeline(
        tasks=[
            double,
            inc,
            collect_results
        ]
    )
    worker.logger.setLevel(-1)
    worker.queue(*range(n))
    worker.join()

    assert len(t) == n
    assert len(filter(lambda x: x[0] == x[1], zip(range(n), t))) == 0
    assert max(t) == (n - 1) * 2 + 1


def test_pipeline_callbacks():
    """
    """
    n = 10

    def double(data, **kwargs):
        return data * 2

    results = []

    worker = pipe.Pipeline(
        tasks=[
            double
        ],
        callbacks=[
            lambda x, y, z: results.append(x)
        ]
    )
    worker.logger.setLevel(-1)
    worker.queue(*range(n))
    worker.join()

    assert len(results) == n
    # ensure all numbers, other than 0, are different
    assert len(filter(lambda x: x[0] == x[1], zip(range(n), results))) == 1
    assert max(results) == (n - 1) * 2


def test_pipeline_context():
    """ Ensure immutable context is passed to tasks and callbacks.

    """
    n = 10

    def double(data, context={}):
        context["test"] = False
        context["data_{}".format(data)] = data * 2
        return data * 2

    context = {"test": True}

    worker = pipe.Pipeline(
        tasks=[
            double
        ],
        callbacks=[
            lambda x, y, z: x
        ],
        context=context
    )
    worker.logger.setLevel(-1)
    worker.queue(*range(n))
    worker.join()

    assert context.get("data_0", None) is None
    assert context.get("test", None) is True
