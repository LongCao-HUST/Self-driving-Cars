# Self-driving-Cars
A.	Xử lý ảnh 
•	Bước 1: Định ngưỡng
o	Tách ảnh đầu vào, sử dụng hàm inRange để tách màu trong không gian màu HSV, thu được ảnh nhị phân
• Bước 2 : Warping Lane
o Tách vùng ảnh quan tâm ra khỏi bức ảnh gốc để xử lý
• Bước 3 : Finding Curve
o Xác định đường tâm
	  a. Vẽ biểu đồ Histogarm
	  b. Tính tổng giá trị pixel theo cột
	  c.  Đặt ngưỡng 
	  d. Xác định điểm – đường cơ sở
  Sau đó , Tính giá trị trung bình với ảnh lấy toàn bộ vùng quan tâm và ảnh lấy 1 phần vùng quan tâm
• Bước 4 : Optimizing Curve
Xử lí kết quả giá trị độ lệch thu được, tính giá trị trung bình của 10 giá trị độ lệch thu được
• Bước 5 : Hoàn thiện
Ghép các ảnh thu được và hiển thị kết quả
• Bước 6 : So sánh
Lấy giá trị độ lệch tính toán được truyền tín hiệu sang Arduino để điều khiển động cơ

B. Điều khiển xe bằng Arduino


 
