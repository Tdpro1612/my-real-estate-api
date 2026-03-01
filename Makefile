.PHONY: format clean help
.PHONY: lint
# Default target
all: help

# Help message
help:
	@echo "Available commands:"
	@echo "  make format       - Format Python code using black and isort/ruff"

format:
	@echo "Formatting Python code..."
	poetry run ruff format . # Code Formatter pep8, Sorts imports library, pylint logic
	@echo "Python code formatted successfully."

fix:
	@echo "fix some python code...."
	poetry run ruff check . --fix
	@echo "fix done with ruff"

lint:
	@echo "Scoring Python code using pylint..."
    # Sử dụng poetry run để đảm bảo pylint được chạy từ môi trường ảo của dự án
    # Chỉ định rõ pyproject.toml làm file cấu hình
    # Chỉ định thư mục mã nguồn chính của bạn (app/) để pylint chỉ kiểm tra code của bạn
	poetry run pylint --rcfile=pyproject.toml app/
	@echo "Python code score with pylint."

# Chạy service FastAPI
run:
	@echo "Starting FastAPI service with Uvicorn..."
	poetry run uvicorn app.main:app --reload
