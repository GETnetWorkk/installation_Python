import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주소록 프로그램")  # 창 제목 설정
        self.setGeometry(100, 100, 450, 350)  # 창 크기와 위치 설정
        self.setStyleSheet("background-color: #f4f4f9;")  # 배경색 변경
        self.address_book = []  # 주소록 데이터를 저장할 리스트
        
        self.initUI()  # UI 초기화 함수 호출

    def initUI(self):
        # 전체 레이아웃 설정
        layout = QVBoxLayout()

        # 제목 라벨 추가
        title_label = QLabel("주소록 관리", self)
        title_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        layout.addWidget(title_label)  # 레이아웃에 제목 라벨 추가

        # 이름 입력 필드 생성
        self.name_input = self.create_input_field("이름을 입력하세요.")
        layout.addWidget(self.name_input)  # 레이아웃에 이름 입력 필드 추가

        # 전화번호 입력 필드 생성
        self.phone_input = self.create_input_field("전화번호를 입력하세요.")
        layout.addWidget(self.phone_input)  # 레이아웃에 전화번호 입력 필드 추가

        # 이메일 입력 필드 생성
        self.email_input = self.create_input_field("이메일을 입력하세요.")
        layout.addWidget(self.email_input)  # 레이아웃에 이메일 입력 필드 추가

        # 주소록에 추가하는 버튼 생성
        self.add_button = QPushButton("주소록에 추가", self)
        self.add_button.setStyleSheet(self.button_style())  # 버튼 스타일 적용
        self.add_button.clicked.connect(self.add_contact)  # 버튼 클릭 시 add_contact 메서드 호출
        layout.addWidget(self.add_button)  # 레이아웃에 버튼 추가

        # 이름으로 검색하는 입력 필드 생성
        self.search_input = self.create_input_field("이름으로 검색하세요.")
        layout.addWidget(self.search_input)  # 레이아웃에 검색 입력 필드 추가

        # 검색 버튼 생성
        self.search_button = QPushButton("검색", self)
        self.search_button.setStyleSheet(self.button_style())  # 버튼 스타일 적용
        self.search_button.clicked.connect(self.search_contact)  # 버튼 클릭 시 search_contact 메서드 호출
        layout.addWidget(self.search_button)  # 레이아웃에 검색 버튼 추가

        # 검색 결과를 표시할 테이블 생성
        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(3)  # 테이블 열 개수 설정
        self.result_table.setHorizontalHeaderLabels(['이름', '전화번호', '이메일'])  # 열 제목 설정
        self.result_table.setStyleSheet("QTableWidget { background-color: #fff; border-radius: 8px; }")  # 테이블 스타일 설정
        layout.addWidget(self.result_table)  # 레이아웃에 테이블 추가

        # 메시지 라벨 추가 (검색 결과가 없거나 오류가 있을 때 보여줄 메시지)
        self.message_label = QLabel("", self)
        self.message_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        self.message_label.setStyleSheet("font-size: 14px; color: #ff4d4d; margin-top: 10px;")
        layout.addWidget(self.message_label)  # 레이아웃에 메시지 라벨 추가

        self.setLayout(layout)  # 설정한 레이아웃을 윈도우에 적용

    def create_input_field(self, placeholder):
        """
        입력 필드를 생성하는 함수.
        :param placeholder: 입력 필드의 placeholder 텍스트
        :return: QLineEdit 위젯
        """
        input_field = QLineEdit(self)
        input_field.setPlaceholderText(placeholder)  # 입력 필드에 placeholder 텍스트 설정
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                margin: 5px 0;
                font-size: 16px;
                border: 2px solid #ccc;
                border-radius: 8px;
                background-color: #fff;
            }
            QLineEdit:focus {
                border: 2px solid #5c8fc2;
            }
        """)  # 입력 필드 스타일 설정
        return input_field

    def button_style(self):
        """
        버튼 스타일을 반환하는 함수.
        :return: QPushButton 스타일 문자열
        """
        return """
            QPushButton {
                padding: 10px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """  # 버튼에 호버, 클릭 효과 스타일 설정

    def add_contact(self):
        """
        주소록에 새로운 연락처를 추가하는 함수.
        """
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        # 모든 필드가 채워졌는지 확인
        if name and phone and email:
            self.address_book.append({'name': name, 'phone': phone, 'email': email})  # 주소록에 연락처 추가
            self.clear_inputs()  # 입력 필드 초기화
            self.update_table()  # 테이블 업데이트
            self.show_message("")  # 메시지 초기화
        else:
            self.show_message("모든 필드를 입력해주세요.")  # 필드가 비어 있으면 경고 메시지 표시

    def search_contact(self):
        """
        이름으로 연락처를 검색하는 함수.
        """
        search_term = self.search_input.text()
        if search_term:
            filtered_contacts = [contact for contact in self.address_book if search_term.lower() in contact['name'].lower()]  # 이름으로 검색
            self.update_table(filtered_contacts)  # 필터링된 연락처를 테이블에 표시
            if not filtered_contacts:
                self.show_message("검색된 결과가 없습니다.")  # 검색 결과가 없으면 메시지 표시
            else:
                self.show_message("")  # 검색된 결과가 있으면 메시지 초기화
        else:
            self.update_table()  # 검색어가 비어 있으면 전체 주소록을 표시

    def update_table(self, contacts=None):
        """
        테이블을 업데이트하는 함수.
        :param contacts: 표시할 연락처 목록
        """
        if contacts is None:
            contacts = self.address_book  # contacts가 None일 경우 전체 주소록으로 설정
        
        self.result_table.setRowCount(len(contacts))  # 테이블의 행 개수 설정
        
        for row, contact in enumerate(contacts):
            # 각 행에 이름, 전화번호, 이메일을 추가
            self.result_table.setItem(row, 0, QTableWidgetItem(contact['name']))
            self.result_table.setItem(row, 1, QTableWidgetItem(contact['phone']))
            self.result_table.setItem(row, 2, QTableWidgetItem(contact['email']))

    def clear_inputs(self):
        """
        입력 필드를 모두 비우는 함수.
        """
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def show_message(self, message):
        """
        메시지 라벨에 텍스트를 설정하는 함수.
        :param message: 표시할 메시지
        """
        self.message_label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddressBook()  # 주소록 프로그램 창 생성
    window.show()  # 창 표시
    sys.exit(app.exec_())  # 애플리케이션 실행
