if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='.env')

import uvicorn
from fastapi import FastAPI
from scripts.core.services import router as endpoint_router


app = FastAPI(title="Fedexxxxxxx", version="1")

app.include_router(endpoint_router, prefix="")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8008)
