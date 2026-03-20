Dự án đề tài Đồ án Nghiên cứu Cử Nhân
Sinh viên : Tạ Quốc Tuấn
MSSV : 20225110

Tên đề tài : Applying Deep Learning Methods to Compute Polygenic Risk Scores for Alzheimer's Disease Prediction

Bối cảnh : 

Phạm vi đề tài : + Trên tập dữ liệu ADNI (Alzheimer Disease Neuroimaging Initiatives) 
                 + Nghiên cứu trên bệnh Alzheimer

Trong tệp này, tôi sẽ liệt kê quy trình xử lý và tiến trình làm đồ án, cũng như cung cấp mã nguồn và quy trình để bạn đọc có thể tái sử dụng . Các tập dữ liệu liên quan sẽ được lưu trữ trên các link google drive. Bạn đọc có nhu cầu sử dụng xin vui lòng xin quyền truy cập qua gmail.

Quy trình bao gồm 3 giai đoạn chính:
- Giai đoạn 1 : Xây dựng pipeline xử lý tập dữ liệu ADNI quy mô lớn
  Mô tả chi tiết nằm trong thư mục Data_processing , bao gồm 4 thư mục con:
   + Genotype_processing : Chứa mô tả chi tiết quy trình xử lý dữ liệu genotype của bộ ADNI
   + Phenotype_processing : Chứa mô tả chi tiết quy trình trích xuất dữ liệu phenotype từ lịch sử khám bệnh của tập ADNI
   + Variant_filtering_jansen : Chứa mã nguồn và các tệp chứa các biến thể có tương quan cao với bệnh ADNI, được sàng lọc từ file metadata trong công bố của Jansen(2019)
   + Merging_dataset : Chứa mã nguồn và mô tả chi tiết quy trình gộp các file đã xử lý để ra được bộ dữ liệu cuối cùng.
- Giai đoạn 2 : Nghiên cứu , thiết kế, xây dựng các phương pháp học máy


(.........)


- Giai đoạn 3 : Thu thập kết quả , so sánh và rút ra kết luận

(.........)