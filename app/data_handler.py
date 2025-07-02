# app/data_handler.py

import pandas as pd
import os

def save_data(data, output_format, filename='output'):
    """스크레이핑한 데이터를 지정된 포맷으로 저장합니다."""
    if not data:
        print("저장할 데이터가 없습니다.")
        return False

    df = pd.DataFrame(data)
    
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)

    try:
        if output_format.lower() == 'csv':
            full_path = f"{filepath}.csv"
            df.to_csv(full_path, index=False, encoding='utf-8-sig')
            print(f"데이터 저장 완료: {full_path}")
        elif output_format.lower() == 'excel':
            full_path = f"{filepath}.xlsx"
            df.to_excel(full_path, index=False)
            print(f"데이터 저장 완료: {full_path}")
        elif output_format.lower() == 'json':
            full_path = f"{filepath}.json"
            df.to_json(full_path, orient='records', indent=4, force_ascii=False)
            print(f"데이터 저장 완료: {full_path}")
        else:
            print(f"지원하지 않는 포맷입니다: {output_format}")
            return False
        return True
    except Exception as e:
        print(f"데이터 저장 중 오류 발생: {e}")
        return False