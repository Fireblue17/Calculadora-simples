import tkinter as tk
from tkinter import messagebox

class Calculator:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Não é possível dividir por zero!")
        return x / y

    def percentage_of(self, total, percentage_value):
        """Calcula a porcentagem de um total."""
        return total * (percentage_value / 100)

    def simple_percentage(self, value):
        """Calcula o valor como porcentagem (x/100)."""
        return value / 100

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora")
        master.resizable(False, False)
        master.configure(bg='black')

        self.calculator = Calculator()
        self.current_expression = ""
        self.input_field = tk.Entry(master, width=30, borderwidth=5, font=('Arial', 16), justify='right',
                                     bg='black', fg='white', insertbackground='white', relief='flat', highlightbackground='gold', highlightcolor='gold', highlightthickness=2)
        self.input_field.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.first_operand = None
        self.operator = None
        self.awaiting_second_operand = False

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '%', '<-', '🍔' # Adicionado '🍔' como um marcador para o botão hambúrguer
        ]

        row_val = 1
        col_val = 0

        button_bg = '#333333'
        button_fg = 'white'
        operator_bg = '#FF9500'
        special_bg = '#505050'

        for button_text in buttons:
            if button_text == '=':
                tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Arial', 14),
                          bg=operator_bg, fg=button_fg, command=self.calculate_result,
                          relief='flat', activebackground='#CC7A00', activeforeground='white').grid(row=row_val, column=col_val, sticky="nsew")
            elif button_text == 'C':
                tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Arial', 14),
                          bg=special_bg, fg=button_fg, command=self.clear_input,
                          relief='flat', activebackground='#404040', activeforeground='white').grid(row=row_val, column=col_val, sticky="nsew")
            elif button_text == '<-':
                tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Arial', 14),
                          bg=special_bg, fg=button_fg, command=self.backspace,
                          relief='flat', activebackground='#404040', activeforeground='white').grid(row=row_val, column=col_val, sticky="nsew")
            elif button_text == '🍔': # Condição para criar o botão hambúrguer
                # Criar um Canvas para o botão hambúrguer
                self.hamburger_canvas = tk.Canvas(self.master, width=30, height=30, bg=special_bg, highlightthickness=0)
                self.hamburger_canvas.grid(row=row_val, column=col_val, sticky="nsew", padx=20, pady=20)

                # Desenhar as três linhas horizontais
                self.hamburger_canvas.create_line(5, 8, 25, 8, fill='white', width=3)
                self.hamburger_canvas.create_line(5, 15, 25, 15, fill='white', width=3)
                self.hamburger_canvas.create_line(5, 22, 25, 22, fill='white', width=3)

                # Associar o clique do mouse ao método show_menu
                self.hamburger_canvas.bind("<Button-1>", self.show_menu)

            elif button_text in ['+', '-', '*', '/']:
                tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Arial', 14),
                          bg=operator_bg, fg=button_fg, command=lambda b=button_text: self.handle_operator(b),
                          relief='flat', activebackground='#CC7A00', activeforeground='white').grid(row=row_val, column=col_val, sticky="nsew")
            elif button_text == '%':
                tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Arial', 14),
                          bg=special_bg, fg=button_fg, command=self.handle_percentage,
                          relief='flat', activebackground='#404040', activeforeground='white').grid(row=row_val, column=col_val, sticky="nsew")
            else:
                tk.Button(self.master, text=button_text, padx=20, pady=20, font=('Arial', 14),
                          bg=button_bg, fg=button_fg, command=lambda b=button_text: self.button_click(b),
                          relief='flat', activebackground='#202020', activeforeground='white').grid(row=row_val, column=col_val, sticky="nsew")

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        for i in range(4):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(row_val + 1):
            self.master.grid_rowconfigure(i, weight=1)

    def show_menu(self, event):
        self.menu = tk.Menu(self.master, tearoff=0, bg='#333333', fg='white',
                            activebackground='#404040', activeforeground='white')
        self.menu.add_command(label="Sobre", command=self.show_about)
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=self.master.quit)

        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def show_about(self):
        messagebox.showinfo("Sobre", "Calculadora Simples\nVersão 1.0\nDesenvolvido com Tkinter")

    def button_click(self, char):
        if self.awaiting_second_operand:
            self.current_expression = str(char)
            self.awaiting_second_operand = False
        else:
            self.current_expression += str(char)
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, self.current_expression)

    def clear_input(self):
        self.current_expression = ""
        self.first_operand = None
        self.operator = None
        self.awaiting_second_operand = False
        self.input_field.delete(0, tk.END)

    def backspace(self):
        """Apaga o último caractere da expressão atual."""
        self.current_expression = self.current_expression[:-1]
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, self.current_expression)

    def handle_operator(self, op):
        try:
            if self.first_operand is None:
                self.first_operand = float(self.current_expression)
                self.operator = op
                self.awaiting_second_operand = True
            else:
                self.calculate_result()
                self.first_operand = float(self.input_field.get())
                self.operator = op
                self.awaiting_second_operand = True
            
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, f"{self.first_operand} {self.operator} ")
            self.current_expression = ""
            
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida antes do operador!")
            self.clear_input()

    def handle_percentage(self):
        try:
            if not self.current_expression:
                return

            current_value = float(self.current_expression)
            result = 0

            if self.operator is None:
                result = self.calculator.simple_percentage(current_value)
            else:
                percentage_amount = self.calculator.percentage_of(self.first_operand, current_value)
                
                if self.operator == '+':
                    result = self.calculator.add(self.first_operand, percentage_amount)
                elif self.operator == '-':
                    result = self.calculator.subtract(self.first_operand, percentage_amount)
                elif self.operator == '*':
                    result = self.calculator.multiply(self.first_operand, self.calculator.simple_percentage(current_value))
                elif self.operator == '/':
                    result = self.calculator.divide(self.first_operand, self.calculator.simple_percentage(current_value))

            self.current_expression = str(result)
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, self.current_expression)
            self.first_operand = result
            self.operator = None
            self.awaiting_second_operand = True

        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida para porcentagem!")
            self.clear_input()
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Não é possível dividir por zero ao calcular porcentagem!")
            self.clear_input()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao calcular porcentagem: {e}")
            self.clear_input()

    def calculate_result(self):
        try:
            if self.first_operand is None or self.operator is None or not self.current_expression:
                return

            second_operand = float(self.current_expression)
            result = 0

            if self.operator == '+':
                result = self.calculator.add(self.first_operand, second_operand)
            elif self.operator == '-':
                result = self.calculator.subtract(self.first_operand, second_operand)
            elif self.operator == '*':
                result = self.calculator.multiply(self.first_operand, second_operand)
            elif self.operator == '/':
                result = self.calculator.divide(self.first_operand, second_operand)
            
            self.current_expression = str(result)
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, self.current_expression)
            
            self.first_operand = result
            self.operator = None
            self.awaiting_second_operand = True

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            self.clear_input()
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Não é possível dividir por zero!")
            self.clear_input()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
            self.clear_input()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()