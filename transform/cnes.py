import pandas as pd
import warnings

PREFIX_MAIN_TBL = "tbEstabelecimento"
PREFIX_BEDS_TBL = "rlEstabComplementar"
PREFIX_INSURANCE_TBL = "rlEstabAtendPrestConv"
PREFIX_CITY_TBL = "tbMunicipio"

COD_GENERAL_HOSPITAL = 5
COD_SPECIALIZED_HOSPITAL = 7

COD_INSURANCE_OWN = 3
COD_INSURANCE_THIRD = 4
COD_INSURANCE_PRIVATE = 5
COD_INSURANCE_PUBLIC = 6


def get_transformed_df(files_dir, version):
    warnings.filterwarnings("ignore")

    file_main = files_dir + "/" + PREFIX_MAIN_TBL + version + ".csv"
    df_main = pd.read_csv(file_main, sep=";", dtype={
        "CO_UNIDADE": str,
        "CO_CNES": str,
        "NU_CNPJ_MANTENEDORA": str,
        "CO_MUNICIPIO_GESTOR": str,
        "CO_CEP": str,
        "NU_TELEFONE": str,
    })
    df_main = df_main.drop(df_main[
        (df_main['TP_UNIDADE'] != COD_GENERAL_HOSPITAL) &
        (df_main['TP_UNIDADE'] != COD_SPECIALIZED_HOSPITAL)
    ].index)
    df_main = df_main[[
        "CO_UNIDADE",
        "CO_CNES",
        "NU_CNPJ_MANTENEDORA",
        "NO_RAZAO_SOCIAL",
        "NO_FANTASIA",
        "CO_MUNICIPIO_GESTOR",
        "CO_CEP",
        "NU_TELEFONE",
        "NO_EMAIL",
    ]]
    df_main = df_main.rename({"CO_MUNICIPIO_GESTOR": "CO_MUNICIPIO"}, axis=1)
    df_main["NO_EMAIL"] = df_main["NO_EMAIL"].str.lower()

    file_city = files_dir + "/" + PREFIX_CITY_TBL + version + ".csv"
    df_city = pd.read_csv(file_city, sep=";", dtype={
        "CO_MUNICIPIO": str,
    })
    df_city = df_city[[
        "CO_MUNICIPIO",
        "NO_MUNICIPIO",
        "CO_SIGLA_ESTADO",
    ]]
    df_city = df_city.groupby(by="CO_MUNICIPIO").agg({
        "NO_MUNICIPIO": "last",
        "CO_SIGLA_ESTADO": "last",
    }).reset_index()

    file_beds = files_dir + "/" + PREFIX_BEDS_TBL + version + ".csv"
    df_beds = pd.read_csv(file_beds, sep=";")
    df_beds = df_beds[[
        "CO_UNIDADE",
        "QT_EXIST",
        "QT_SUS",
    ]]
    df_beds["QT_SUS"] = df_beds.apply(lambda row: 1 if row["QT_SUS"] > 0 else 0, axis=1)
    df_beds = df_beds.groupby(by="CO_UNIDADE").agg({
        "QT_EXIST": "sum",
        "QT_SUS": "max",
    }).reset_index()

    file_insurance = files_dir + "/" + PREFIX_INSURANCE_TBL + version + ".csv"
    df_insurance = pd.read_csv(file_insurance, sep=";")
    df_insurance = df_insurance.drop(df_insurance[
        (df_insurance['CO_CONVENIO'] != COD_INSURANCE_OWN) &
        (df_insurance['CO_CONVENIO'] != COD_INSURANCE_THIRD) &
        (df_insurance['CO_CONVENIO'] != COD_INSURANCE_PRIVATE) &
        (df_insurance['CO_CONVENIO'] != COD_INSURANCE_PUBLIC)
    ].index)
    df_insurance = df_insurance[[
        "CO_UNIDADE",
    ]]
    df_insurance["Atende Convênio?"] = 1
    df_insurance = df_insurance.groupby(by="CO_UNIDADE").agg({
        "Atende Convênio?": "max",
    }).reset_index()

    df_merge = df_main.merge(df_beds, how="inner", on="CO_UNIDADE")
    df_merge = df_merge.merge(df_insurance, how="left", on="CO_UNIDADE")
    df_merge = df_merge.merge(df_city, how="left", on="CO_MUNICIPIO")
    df_merge["Atende Convênio?"] = df_merge["Atende Convênio?"].fillna(0)
    df_merge["Atende Convênio?"] = df_merge["Atende Convênio?"].astype(int)

    df_merge = df_merge.rename({
        "CO_CNES": "Código CNES",
        "NU_CNPJ_MANTENEDORA": "CNPJ",
        "NO_RAZAO_SOCIAL": "Razão Social",
        "NO_FANTASIA": "Nome Fantasia",
        "CO_CEP": "CEP",
        "NU_TELEFONE": "Telefone",
        "NO_EMAIL": "Email",
        "QT_EXIST": "Leitos",
        "QT_SUS": "Atende SUS?",
        "NO_MUNICIPIO": "Município",
        "CO_SIGLA_ESTADO": "UF",
    }, axis=1)

    df_merge = df_merge[[
        "Nome Fantasia",
        "Razão Social",
        "CNPJ",
        "Código CNES",
        "Município",
        "UF",
        "CEP",
        "Telefone",
        "Email",
        "Leitos",
        "Atende SUS?",
        "Atende Convênio?",
    ]]
    return df_merge.sort_values(by=["UF"])


def __get_file_name(files_dir, name, version):
    return files_dir + "/" + name + version + ".csv"
