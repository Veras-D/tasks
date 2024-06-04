from flet import *
import sqlite3


class Gerenciartarefas:
    def __init__(self, page:Page):
        self.page = page
        # self.page.bgcolor = colors.DEEP_PURPLE
        self.page.title = "Gerenciador de Tarefas Time - 25"
        self.page.scroll = True
        self.db_execute("CREATE TABLE IF NOT EXISTS tasks(tarefa, prazo, area, nota)")
        self.results = self.db_execute("SELECT * FROM tasks")
        self.container_design = self.tasks_container_design()
        self.main_page()
    
    
    def db_execute(self, query, param = []):
        with sqlite3.connect('tarefas.db') as con:
            cur = con.cursor()
            cur.execute(query, param)
            con.commit()
            return cur.fetchall()
    
    
    def tasks_container_design(self):
        conteudo_design = Container(content=[])
        conteudo_design = [Container(
            content=Column([
                Text(f"Tasks: {res[0]}\nPrazo: {res[1]}\nNota: {res[3]}" if res[3] else f"Tasks: {res[0]}\nPrazo: {res[1]}", size=17),
                Divider(height=1, color="white")
                ] 
            )
        ) for res in self.results if res[2] == "Backend"]

        self.container_design = Container(
            height=self.page.height * 0.8,
            content=Column(
                controls=conteudo_design,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            scroll=True
            ),
            padding=10,
        )
        return self.container_design
    
    def add_task(self, input_task, display_data, display_hora, input_area, input_note):
        task = input_task.value
        prazo = f"{display_data.value} - {display_hora.value}"
        area = input_area.value
        nota = input_note.value
        if str(task).split()[0] != '' and str(display_data.value) != '' and str(display_hora.value) != '' and area is not None:
            self.db_execute(query='INSERT INTO tasks VALUES(?,?,?,?);', param=(task, prazo, area, nota))
            input_task.value = None
            display_data.value = None
            display_hora.value = None
            input_area.value = None
            input_note.value = None
        else:
            # Colocar alerta
            pass
        self.container_design.clean()
        self.results = self.db_execute("SELECT * FROM tasks")
        self.update_tasks_list()
        self.page.update()
    
    def update_tasks_list(self):
        tasks_design = self.tasks_container_design()
        self.page.controls.pop(-1)
        self.page.add(tasks_design)
        self.page.update()
        
    def main_page(self):
        def change_date(e):
            display_data.value = date_picker.value.date()
            self.page.update()
            
        def change_time(e):
            display_hora.value = f"{time_picker.value.hour:02}:{time_picker.value.minute:02}"
            self.page.update()

        date_picker = DatePicker(
            on_change=change_date,
        )
        time_picker = TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=change_time,
        )
        self.page.overlay.append(date_picker)
        self.page.overlay.append(time_picker)
        
        input_task = TextField(hint_text="Adicionar Task")
        display_data = TextField(hint_text="Prazo da Tasks: Data", read_only=True, width=200, text_align="center")
        input_data= FloatingActionButton(icon=icons.CALENDAR_MONTH, on_click=lambda _: date_picker.pick_date())
        display_hora = TextField(hint_text="Prazo da Tasks: Hora", read_only=True, width=200, text_align="center")
        input_hora = FloatingActionButton(icon=icons.ACCESS_TIME, on_click=lambda _: time_picker.pick_time())
        input_area = Dropdown(hint_text="Escolha a Area da Tasks", width=225,
                options=[
                dropdown.Option("Backend"),
                dropdown.Option("Dados"),
                dropdown.Option("Design"),
                dropdown.Option("Frontend"),
                dropdown.Option("Jogos")
            ]
        )
        input_note = TextField(hint_text="Adicionar Nota a Task...", multiline=True, expand=True)
        
        
        input_bar = Row(
            controls=[
                    input_task,
                    display_data,
                    input_data,
                    display_hora,
                    input_hora,
                    input_area,
                    FloatingActionButton(icon=icons.ADD, on_click=lambda _:self.add_task(input_task, display_data, display_hora, input_area, input_note))
                ]
        )
        field_input_note = Row([
            input_note
        ])
        
        tasks_design = self.tasks_container_design()  # Notas deve haver um desse para cada area e eles devem ser adicionados na coluna do container
        
        areas = Row(
            controls=
            [
                Container(
                    content=Text("Back-End", weight=FontWeight.BOLD, size=25),
                    margin=10,
                    padding=10,
                    alignment=alignment.top_center,
                    bgcolor="#292D2C",
                    width=350,
                    height=750,
                    border_radius=10,
                ),
                Container(
                    content=Text("Dados", weight=FontWeight.BOLD, size=25),
                    margin=10,
                    padding=10,
                    alignment=alignment.top_center,
                    bgcolor="#292D2C",
                    width=350,
                    height=750,
                    border_radius=10,
                ),
                Container(
                    content=Column(
                        controls=[
                                Text("Design", weight=FontWeight.BOLD, size=25),
                                Container(height=10),
                                tasks_design,
                            ]
                        ),
                    margin=10,
                    padding=10,
                    alignment=alignment.top_center,
                    bgcolor="#292D2C",
                    width=350,
                    height=750,
                    border_radius=10,
                ),
                Container(
                    content=Text("Front-End", weight=FontWeight.BOLD, size=25),
                    margin=10,
                    padding=10,
                    alignment=alignment.top_center,
                    width=350,
                    height=750,
                    border_radius=10,
                    bgcolor="#292D2C",
                ),
                Container(
                    content=Text("Jogos", weight=FontWeight.BOLD, size=25),
                    margin=10,
                    padding=10,
                    alignment=alignment.top_center,
                    width=350,
                    height=750,
                    border_radius=10,
                    bgcolor="#292D2C",
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        )

        self.page.add(input_bar, field_input_note, areas, tasks_design)
        self.page.update()


app(target=Gerenciartarefas, view=WEB_BROWSER)
# app(target=Gerenciartarefas)
