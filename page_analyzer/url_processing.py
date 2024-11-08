import psycopg2
from flask import render_template, redirect, url_for
from typing import List, Optional, Tuple

from .flash_messages import handle_flash_messages
from .database import (add_url, find_by_name)
from .url_validator import validate_url, normalize_url


def process_url(url_from_request: str, cursor) \
        -> Tuple[Optional[dict], Optional[list]]:
    """
    Processes the URL, checking it for errors and adding it to the database.
    """
    result = validate_url(url_from_request)
    if not result.is_valid():
        return None, result.errors

    new_url = normalize_url(url_from_request)

    try:
        url_info = add_url(cursor, new_url)
        return url_info, None
    except psycopg2.errors.UniqueViolation:
        return find_by_name(new_url), None


def process_url_submission(cursor, url_from_request: str) \
        -> Tuple[List[str], bool, Optional[int]]:
    """
    Processes the submitted URL, checking it
    and adding it to the database if there are no duplicates.
    """
    result = validate_url(url_from_request)
    url_id = None
    is_duplicate = False

    if result.is_valid():
        new_url = normalize_url(url_from_request)
        try:
            add_url(cursor, new_url)
            cursor.execute("SELECT * FROM urls WHERE name = %s", (new_url,))
            url_info = cursor.fetchone()
            if url_info:
                url_id = url_info.id
        except psycopg2.errors.UniqueViolation:
            is_duplicate = True
            url = find_by_name(new_url)
            if url:
                url_id = url.id

    return result.errors, is_duplicate, url_id


def set_flash_messages(cursor, form_data: dict) -> Tuple[str, int]:
    """
    Process the URL submission, handle flash messages, and return response.
    """
    url_from_request = form_data.get('url', '')
    errors, is_duplicate, url_id = (
        process_url_submission(cursor, url_from_request))

    handle_flash_messages(errors, is_duplicate, url_id)

    if errors:
        return render_template('index.html'), 422
    if is_duplicate or url_id:
        return redirect(url_for('get_one_url', id=url_id))

    return render_template('index.html'), 500