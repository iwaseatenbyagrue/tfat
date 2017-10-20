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
