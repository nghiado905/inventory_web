import pandas as pd

def sum_of_type(df):
    df['Tổng Giá trị'] = df['Giá bán'] * df['Số lượng']
    result = df.groupby('Mã hàng')['Tổng Giá trị'].sum().reset_index()
    # result = df.groupby('Mã hàng')['Giá bán'].sum().reset_index()

    return result.to_dict(orient='records')  # Chuyển đổi thành danh sách các từ điển

def sum_of_name(df):
    df['Tổng Giá trị'] = df['Giá bán'] * df['Số lượng']
    result = df.groupby('Tên hàng')['Tổng Giá trị'].sum().reset_index()
    return result.to_dict(orient='records')  # Chuyển đổi thành danh sách các từ điển

def sum_today(df):
    df['Tổng Giá trị'] = df['Giá bán'] * df['Số lượng']
    sum_of_today = df['Tổng Giá trị'].sum()
    return sum_of_today