# ecqopcd

**ecqopcd** (est-ce qu’on peut courir demain) is a Web app for joggers in Paris
that check weather and pollution indices for the day after and tells if it’s ok
to go out jogging.

*est-ce qu’on peut courir demain* means “can we run tomorrow” in French. The
app was written for a personal need and is live on [estcequonpeutcourirdemain.fr](http://estcequonpeutcourirdemain.fr).

## Run

To run the app locally, you need Redis and Python 2.7 with virtualenv. Set up
the local environment:

    virtualenv --distribute venv
    source venv/bin/activate
    pip install -qr requirements.txt

Then make sure a Redis server is running locally, and launch the app:

    make run

You can now open your browser at `localhost:8000`.
