FROM python:3.10-bullseye


# System deps:
RUN pip install "poetry==1.4.2"

# Copy only requirements to cache them in docker layer

# Creating folders, and files for a project:
COPY . .
COPY poetry.lock pyproject.toml /

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install 



EXPOSE 5000

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]