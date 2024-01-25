from fastapi import FastAPI

app = FastAPI()
app.title = "My movie API"
app.version = "0.0.1"


@app.get('/', tags=["Home"])
def message():
    '''Hello World'''
    return "Hello world"
