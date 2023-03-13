Installation
=========================

$ pip install fastapi

You will also need an ASGI server, for production such as Uvicorn or Hypercorn.

$ pip install uvicorn==0.16.0


Run the server with:
---------------------------------
python -m uvicorn main:app --reload