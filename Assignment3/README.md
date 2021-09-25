# CS106
Bài tập 3: Using OR_tool and Genetic Algorithm to solve Knapsack
## Thành phần và thư mục báo cáo quan trọng
*`_GA_Results_`:file chứa kết quả chạy từng test của mỗi group của Genetic
*`_or_Tools_Results_`:file chứa kết quả chạy từng test của mỗi group của OR
*`GA.py`:cài đặt thuật toán GA và kết quả chạy
*`OR_Tools.py`: cài đặt OR_Tools và kết quả chạy
*`test_case_pick.py`: chọn test từ bộ test kblib
*`write_csv.py`: ghi file csv từ folder chứa kết quả
*`CS106_assignment3.pdf`:file báo cáo 
*`n_.csv`: là các tập tin csv lưu trữ kết quả chạy của 
	OR(trong file resultOR có 2 sheet lưu kết quả chạy và so sánh kết quả với Genetic) 
	Genetic(50,100,200,300)
*`tex-assignment`:file latex cho báo cáo
##Các bước chạy
step 1: đầu tiên ta chạy ` python test_case_pick.py` để chọn testcase
step 2: chạy một trong 2 file (GA  hoặc OR_Tools).py để thực hiện thuật toán (vd: python GA.py)
step 3: Kết quả được lưu ở folder tương ứng,để export ra file csv ta sẽ chạy `python write_csv.py`
(để xuất ra file csv cần xóa kết quả ở folder lưu kết quả cũ)