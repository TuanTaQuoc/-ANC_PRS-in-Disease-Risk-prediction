import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import warnings
from sklearn.pipeline import Pipeline

# ==========================================
# BƯỚC 1: TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING)
# ==========================================

print("1. Đang tải và tiền xử lý dữ liệu...")
# Đọc tập Train/Val (998 bản ghi) đã được chia từ trước
df_train = pd.read_csv('train_val_dataset_1e-8.txt', sep=' ')
X_train_raw = df_train.drop(columns=['RID', 'Phenotype']).values
y_train = df_train['Phenotype'].values

# Lưu lại danh sách tên các biến thể gen để dùng cho Bước 6 (Feature Importance)
feature_names = df_train.drop(columns=['RID', 'Phenotype']).columns.tolist()

print(f"Kích thước tập X_train: {X_train_raw.shape}")
print(f"Kích thước tập y_train: {y_train.shape}")

# 2. Khởi tạo Pipeline đóng gói cả Scaler và Model

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('log_reg', LogisticRegression(solver='saga', max_iter=5000, random_state=42 , verbose=1))
])

# ==========================================
# BƯỚC 3: THIẾT LẬP MÔ HÌNH VÀ LƯỚI SIÊU THAM SỐ
# ==========================================

# Định nghĩa không gian tìm kiếm siêu tham số
param_grid = {
    # Thử nghiệm cả L1 (giảm nhiễu/chọn đặc trưng) và L2 (ngăn chặn overfit)
    'log_reg__penalty': ['l2'],
    # C là hệ số nghịch đảo của Regularization (C càng nhỏ, phạt càng mạnh)
    'log_reg__C': [0.005]
}
penalty = param_grid['log_reg__penalty']
C = param_grid['log_reg__C']
print("Đã thiết lập xong không gian tham số:")
print(param_grid)


cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ==========================================
# BƯỚC 4: HUẤN LUYỆN VÀ TÌM KIẾM SIÊU THAM SỐ
# ==========================================
print("\n4. Đang tìm kiếm siêu tham số tối ưu (GridSearchCV)...")
grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=cv_strategy,
    scoring='roc_auc',  # Tối ưu hóa dựa trên ROC-AUC
    n_jobs=-1,          # Sử dụng toàn bộ số luồng CPU để chạy nhanh hơn
    verbose=3
)
grid_search.fit(X_train_raw, y_train)

print(f"\n=> Tham số tốt nhất: {grid_search.best_params_}")
print(f"=> ROC-AUC tốt nhất trên tập Validation: {grid_search.best_score_:.4f}")

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import numpy as np

# ==========================================
# BƯỚC 6: ĐÁNH GIÁ TRÊN TẬP HOLD-OUT TEST
# ==========================================
print("\n--- BƯỚC 6: ĐÁNH GIÁ TRÊN TẬP HOLD-OUT TEST ---")

# 1. Đọc dữ liệu tập Test
df_test = pd.read_csv('test_dataset_1e-8.txt', sep=' ')
X_test_raw = df_test.drop(columns=['RID', 'Phenotype']).values
y_test = df_test['Phenotype'].values

# 2. Lấy mô hình tốt nhất từ GridSearchCV (chính là toàn bộ Pipeline)
best_pipeline = grid_search.best_estimator_

# 3. Dự đoán trên tập Test
# Đưa trực tiếp X_test_raw vào. Pipeline sẽ tự động Scale -> sau đó đưa vào Logistic Regression
y_pred = best_pipeline.predict(X_test_raw)
y_pred_proba = best_pipeline.predict_proba(X_test_raw)[:, 1]

# 4. Tính toán và in các chỉ số
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc = roc_auc_score(y_test, y_pred_proba)
cm = confusion_matrix(y_test, y_pred)

print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc:.4f}")
print(f"Confusion Matrix:\n{cm}")


# ==========================================
# BƯỚC 7: KHAI THÁC ĐẶC TRƯNG TỪ PIPELINE
# ==========================================
print("\n--- BƯỚC 7: TOP 10 GEN QUAN TRỌNG NHẤT ---")

# Để lấy trọng số (coef_), ta phải trỏ vào mô hình Logistic Regression nằm BÊN TRONG Pipeline
best_log_reg = best_pipeline.named_steps['log_reg']
weights = best_log_reg.coef_[0]

# Lấy lại tên cột từ df_train
feature_names = df_train.drop(columns=['RID', 'Phenotype']).columns.tolist()

feature_importance = pd.DataFrame({
    'Gene_Variant': feature_names,
    'Weight': weights,
    'Abs_Weight': np.abs(weights)
}).sort_values(by='Abs_Weight', ascending=False)

print(feature_importance[['Gene_Variant', 'Weight']].head(10).to_string(index=False))

# Xuất toàn bộ danh sách trọng số ra file CSV
output_csv = f'FI_{penalty}_c={C}.csv'
feature_importance.drop(columns=['Abs_Weight']).to_csv(output_csv, index=False)
print(f"\n=> Đã xuất toàn bộ trọng số của các gen ra file: {output_csv}")

