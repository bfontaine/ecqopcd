# ecqopcd

**ecqopcd** (est-ce qu’on peut courir demain) is a Web app for joggers in Paris
that checks weather and pollution indices for the day after and tells if it’s
ok to go out jogging.

*est-ce qu’on peut courir demain* means “can we run tomorrow” in French. The
app was written for a personal need and is live on [estcequonpeutcourirdemain.fr](http://estcequonpeutcourirdemain.fr).

The pollution indices fetcher was released as a standalone library,
[Firapria][].

[Firapria]: https://github.com/bfontaine/firapria

## Run

You need Redis and Python 2.7 with virtualenv to run the app locally, as well
as a [Previmeteo](http://previmeteo.com/) API key. Set up the local
environment:

    virtualenv --distribute venv
    source venv/bin/activate
    pip install -qr requirements.txt
    export PREVIMETEO_KEY='put-your-api-key-here'

Then make sure a Redis server is running locally, and launch the app:

    make run

You can now open your browser at `localhost:8000`.
