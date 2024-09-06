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



def sum_of_name(df):
    return len(df)


def count_product(df):
    df['Số lượng'] = pd.to_numeric(df['Số lượng'])
    return df['Số lượng'].sum()

def sum_today(df):
    df['Tổng thu'] =  pd.to_numeric(df['Thu']).sum()
    df['Tổng chi'] = pd.to_numeric(df['Chi']).sum()
    sum_of_today = df['Tổng thu'] - df['Tổng chi']
    return sum_of_today[0] # Chuyển đổi thành danh sách các từ điển
