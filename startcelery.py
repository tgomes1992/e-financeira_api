import os



os.system("celery -A efinapi worker --pool=threads --concurrency=8")