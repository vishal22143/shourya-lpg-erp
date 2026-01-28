from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from data.db import get_conn

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/office')
def office_dashboard(request: Request):
    # TEMP SAFE DEFAULTS (BPCL STRUCTURE)
    filled_142 = 0
    empty_142 = 0
    filled_5 = 0
    empty_5 = 0
    filled_19 = 0
    empty_19 = 0
    defective = 0

    last_update = 'Not entered yet'
    entered_by = '-'

    # OPTIONAL: read latest godown entry if exists
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                filled_142, empty_142,
                filled_5, empty_5,
                filled_19, empty_19,
                defective,
                created_at, user
            FROM godown_physical
            ORDER BY created_at DESC
            LIMIT 1
        """)
        row = cur.fetchone()
        conn.close()

        if row:
            (
                filled_142, empty_142,
                filled_5, empty_5,
                filled_19, empty_19,
                defective,
                last_update, entered_by
            ) = row
    except:
        pass  # DB may not have columns yet – UI must still work

    grand_total = (
        filled_142 + empty_142 +
        filled_5 + empty_5 +
        filled_19 + empty_19 +
        defective
    )

    return templates.TemplateResponse(
        'office_dashboard.html',
        {
            'request': request,
            'filled_142': filled_142,
            'empty_142': empty_142,
            'filled_5': filled_5,
            'empty_5': empty_5,
            'filled_19': filled_19,
            'empty_19': empty_19,
            'defective': defective,
            'grand_total': grand_total,
            'last_update': last_update,
            'entered_by': entered_by
        }
    )
