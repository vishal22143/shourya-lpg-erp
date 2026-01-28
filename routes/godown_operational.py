from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date
from data.db import get_conn

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/godown")
def godown_operational(request: Request):
    return templates.TemplateResponse("godown_operational.html", {"request": request})

@router.post("/godown/physical/save")
def save_physical(
    filled_ubhi: int = Form(0),
    filled_adavi: int = Form(0),
    filled_adhik: int = Form(0),
    defective: int = Form(0),

    er_ubhi: int = Form(0),
    er_adavi: int = Form(0),
    er_adhik_single: int = Form(0),
    er_adhik_double: int = Form(0),
    er_akheri: int = Form(0),

    el_ubhi: int = Form(0),
    el_adavi: int = Form(0),
    el_adhik_single: int = Form(0),
    el_adhik_double: int = Form(0),
    el_akheri: int = Form(0),
):
    filled_total = filled_ubhi * filled_adavi + filled_adhik
    full_total = filled_total + defective

    def empty_side(ubhi, adavi, add_single, add_double, akheri):
        base = ubhi * adavi * 2
        additional = add_single + (add_double * 2)
        return base + additional + akheri

    empty_right = empty_side(er_ubhi, er_adavi, er_adhik_single, er_adhik_double, er_akheri)
    empty_left  = empty_side(el_ubhi, el_adavi, el_adhik_single, el_adhik_double, el_akheri)
    empty_total = empty_right + empty_left

    conn = get_conn()
    conn.execute(
        '''
        INSERT INTO godown_physical
        (entry_date, section,
         filled_rows, filled_cols, filled_loose,
         empty_rows, empty_cols, empty_loose,
         defective, remark)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ''',
        (
            date.today().isoformat(),
            "PHYSICAL",
            filled_ubhi, filled_adavi, filled_adhik,
            empty_total, 0, 0,
            defective,
            "AUTO – GODOWN PHYSICAL"
        )
    )
    conn.commit()
    conn.close()

    return {"full_stock": full_total, "empty_stock": empty_total}
