# Self-driving-Cars
## A.	Xử lý ảnh 
### Bước 1: Định ngưỡng
- Tách ảnh đầu vào, sử dụng hàm inRange để tách màu trong không gian màu HSV, thu được ảnh nhị phân
### Bước 2 : Warping Lane
- Tách vùng ảnh quan tâm ra khỏi bức ảnh gốc để xử lý
### Bước 3 : Finding Curve
- Xác định đường tâm
	  - Vẽ biểu đồ Histogarm
	  - Tính tổng giá trị pixel theo cột
	  -  Đặt ngưỡng 
	  - Xác định điểm – đường cơ sở
  Sau đó , Tính giá trị trung bình với ảnh lấy toàn bộ vùng quan tâm và ảnh lấy 1 phần vùng quan tâm
### Bước 4 : Optimizing Curve
Xử lí kết quả giá trị độ lệch thu được, tính giá trị trung bình của 10 giá trị độ lệch thu được
Từ đó : So sánh tổng pixel 2 bên trái phải để đưa hình dạng của đường
![image](https://github.com/LongCao-HUST/Self-driving-Cars/blob/41114e7ae4e78cc6149539e8412a136a1f526629/minhhoa.png)
### Bước 5 : Hoàn thiện
Ghép các ảnh thu được và hiển thị kết quả
### Bước 6 : So sánh
Lấy giá trị độ lệch tính toán được truyền tín hiệu sang Arduino để điều khiển động cơ

# B. Điều khiển xe bằng Arduino
![image](https://github.com/LongCao-HUST/Self-driving-Cars/blob/41114e7ae4e78cc6149539e8412a136a1f526629/resulft%20control.png)

 
