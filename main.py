import datetime
from fastapi import FastAPI, Form, Path, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Order:
    def __init__(self, number, date, tehnica, model, problema, FIO, phone, status):
        self.number = number
        self.date = date
        self.tehnica = tehnica
        self.model = model
        self.problema = problema
        self.FIO = FIO
        self.phone = phone
        self.status = status


class OrderRepository:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def get_all_orders(self):
        return self.orders

    def get_order_by_number(self, number):
        for order in self.orders:
            if order.number == number:
                return order
        return None

    def update_order(self, number, updated_order):
        for i, order in enumerate(self.orders):
            if order.number == number:
                self.orders[i] = updated_order
                return True
        return False

    def delete_order(self, number):
        self.orders = [order for order in self.orders if order.number != number]


repo = OrderRepository()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "orders": repo.get_all_orders()})

@app.post("/add")
async def add_order(number: float = Form(...), date: str = Form(...), tehnica: str = Form(...), model: str = Form(...), problema: str = Form(...), FIO: str = Form(...), phone: str = Form(...), status: str = Form(...)):
    try:
        if repo.get_order_by_number(number):
            return JSONResponse({"error": "Заявка под таким номером уже есть"}, status_code=400)
            
        date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        new_order = Order(number, date_object, tehnica, model, problema, FIO, phone, status)
        repo.add_order(new_order)
        return {"message": "Заявка добавлена!"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@app.get("/order/{number}", response_class=HTMLResponse)
async def view_order(request: Request, number: float = Path(...)):
    order = repo.get_order_by_number(number)
    if order:
        return templates.TemplateResponse("view_order.html", {"request": request, "order": order})
    return JSONResponse({"error": ""}, status_code=404)

@app.put("/order/{number}")
async def update_order(number: float = Path(...), date: str = Form(...), tehnica: str = Form(...), model: str = Form(...), problema: str = Form(...), FIO: str = Form(...), phone: str = Form(...), status: str = Form(...)):
    try:
        date_object = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        updated_order = Order(number, date_object, tehnica, model, problema, FIO, phone, status)
        if repo.update_order(number, updated_order):
            return {"message": "Заявка обнавлена!"}
        return JSONResponse({"error": ""}, status_code=404)
    except Exception:
        return JSONResponse({"error": "Ошибка введения даты"}, status_code=400)

@app.delete("/order/{number}")
async def delete_order(number: float = Path(...)):
    if repo.get_order_by_number(number):
        repo.delete_order(number)
        return {"message": "Заявка удалена!"}
    return JSONResponse({"error": ""}, status_code=404)