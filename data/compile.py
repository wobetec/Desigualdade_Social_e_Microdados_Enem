import pandas as pd


def load_data():
    '''
    Load the ENEM 2023 dataset.
    '''
    print('Loading data...')
    df = pd.read_csv('./microdados_enem_2023/DADOS/MICRODADOS_ENEM_2023.csv', encoding='ISO-8859-1', sep=';')
    print('Data loaded successfully!')
    return df

def compile_data():
    '''
    Compile a sample of 10% of the data from the ENEM 2023 dataset and save it to a feather file for faster loading and exploration.
    ''' 
    print('Compiling data...')
    print('This may take a while...')
    df = load_data()
    n = df.shape[0]
    n_sample = int(n * 0.1)
    print(f'Sampling {n_sample} rows...')
    df_sample = df.sample(n_sample)
    print('Saving sample to feather file...')
    df_sample.to_feather('./compiled.feather')
    print('Data compiled successfully!')

def filter_data():
    '''
    Filter the ENEM 2023 dataset to keep only the columns and rows that are relevant for the analysis.
    '''
    print('Filtering data...')
    print('This may take a while...')
    df = load_data()
    original_data_shape = df.shape
    print('Original data shape: ', original_data_shape)

    wanted_columns = [
        'TP_ST_CONCLUSAO',
        'TP_ANO_CONCLUIU',
        'IN_TREINEIRO',

        'SG_UF_PROVA',

        'NU_NOTA_CN',
        'NU_NOTA_CH',
        'NU_NOTA_LC',
        'NU_NOTA_MT',
        'NU_NOTA_REDACAO',

        'Q001', 'Q002', 'Q003', 'Q004', 'Q005',
        'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
        'Q011', 'Q012', 'Q013', 'Q014', 'Q015',
        'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
        'Q021', 'Q022', 'Q023', 'Q024', 'Q025'
   ]
    
    end_columns = [
        'SG_UF_PROVA',

        'NU_NOTA',
        
        'Q001', 'Q002', 'Q003', 'Q004', 'Q005',
        'Q006', 'Q007', 'Q008', 'Q009', 'Q010',
        'Q011', 'Q012', 'Q013', 'Q014', 'Q015',
        'Q016', 'Q017', 'Q018', 'Q019', 'Q020',
        'Q021', 'Q022', 'Q023', 'Q024', 'Q025'
    ]
    
    df = df[wanted_columns]
    df = df[df.IN_TREINEIRO == 0]
    for prova in ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT']:
        df = df[df[prova] != 0]
        df = df[df[prova].notnull()]
    df['NU_NOTA'] = df[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']].mean(axis=1)
    df = df[df.TP_ST_CONCLUSAO != 4]
    df = df[df.TP_ANO_CONCLUIU != 0]

    df = df[df.Q001 != 'H']
    df = df[df.Q002 != 'H']
    df = df[df.Q003 != 'F']
    df = df[df.Q004 != 'F']

    df = df[end_columns]

    end_data_shape = df.shape

    print('Filtered data shape: ', end_data_shape)
    print(f'Percentage of data kept: {end_data_shape[0] / original_data_shape[0] * 100:.2f}')
    print('Data filtered successfully!')

    df.to_feather('./filtered.feather')


if __name__ == '__main__':
    filter_data()
