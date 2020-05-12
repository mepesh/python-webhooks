import pandas as pd
import requests, json
import numpy as np

#python-webhooks-fcns
def municipal_district_df():
    url_dis = "https://data.nepalcorona.info/api/v1/districts"
    response_dis = requests.get(url_dis)
    total_dis = json.loads(response_dis.text)
    df =pd.DataFrame(total_dis)
    df = df[['id','title_en']]
    df = df.rename(columns={'id': 'district'})

    url_mun = "https://data.nepalcorona.info/api/v1/municipals/"
    response_mun = requests.get(url_mun)
    total_mun = json.loads(response_mun.text)
    df_mun =pd.DataFrame(total_mun)
    df_mun = df_mun[['id','title','type','district']]

    df_mun_dis = df_mun.merge(df, on='district')
    df_mun_dis = df_mun_dis[['id','title','type','title_en']]
    df_mun_dis = df_mun_dis.rename(columns={'id': 'municipality'})

    return (df_mun_dis)

def create_covid_df():
    df_mun_dis = municipal_district_df()
    url_cov = "https://data.nepalcorona.info/api/v1/covid"
    response_cov = requests.get(url_cov)
    total_cov = json.loads(response_cov.text)
    df_cov =pd.DataFrame(total_cov)
    mergedDf = df_cov.merge(df_mun_dis, on='municipality')
    mergedDf = mergedDf[['province','district','municipality','title','type_y','title_en','gender','age','currentState']]
    mergedDf = mergedDf.rename(columns={'province': 'provience'})
    mergedDf = mergedDf.rename(columns={'currentState': 'currentstate'})
    return(mergedDf)

def affected_summary():
    mergedDf = create_covid_df()
    p = mergedDf['provience'].unique().tolist()
    m = mergedDf['municipality'].unique().tolist()
    d = mergedDf['district'].unique().tolist()
    text = str(len(p))+" Provience "+str(len(m))+" Municiapls and "+str(len(d))+" Districts Affected So Far !"
    return (text)

def provience_all_summary():
    df = create_covid_df()
    abr1 = df[(df["provience"] == 1) & (df["currentstate"] == "recovered")]
    t1 = df[(df["provience"] == 1)]
    abr2 = df[(df["provience"] == 2) & (df["currentstate"] == "recovered")]
    t2 = df[(df["provience"] == 2)]
    abr3 = df[(df["provience"] == 3) & (df["currentstate"] == "recovered")]
    t3 = df[(df["provience"] == 3)]
    abr4 = df[(df["provience"] == 4) & (df["currentstate"] == "recovered")]
    t4 = df[(df["provience"] == 4)]
    abr5 = df[(df["provience"] == 5) & (df["currentstate"] == "recovered")]
    t5 = df[(df["provience"] == 5)]
    abr6 = df[(df["provience"] == 6) & (df["currentstate"] == "recovered")]
    t6 = df[(df["provience"] == 6)]
    abr7 = df[(df["provience"] == 7) & (df["currentstate"] == "recovered")]
    t7 = df[(df["provience"] == 7)]
    
    data ="Province 1: "+str(len(t1))+"("+str(len(abr1))+")"+"\n"+"Province 2: "+str(len(t2))+"("+str(len(abr2))+")"+"\n"+"Provience 3: "+str(len(t3))+"("+str(len(abr3))+")"+"\n"+"Provience 4: "+str(len(t4))+"("+str(len(abr4))+")"+"\n"+"Provience 5: "+str(len(t5))+"("+str(len(abr5))+")"+"\n"+"Provience 6: "+str(len(t6))+"("+str(len(abr6))+")"+"\n"+"Provience 7: "+str(len(t7))+"("+str(len(abr7))+")"+"\n"

    return(data)

def district_all_summary():
    df = create_covid_df()
    ld = df['title_en'].unique()
    data = "District Affected\n"
    for i in range(len(ld)):
        abr = df[(df["title_en"] == ld[i]) & (df["currentstate"] == "recovered")]
        total = df[(df["title_en"] == ld[i])]
        data+= ""+ld[i]+": "+str(len(total))+" ("+str(len(abr))+") \n"
        
    print(data)

    return(data)

#----end--
def get_nepal_cumulative(country):
    death_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    )

    confirmed_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    )
    recovered_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    )
    country_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
    )

    nepal_cases = confirmed_df.loc[confirmed_df["Country/Region"] == country]
    nepal_recovered = recovered_df.loc[recovered_df["Country/Region"] == country]
    nepal_death = death_df.loc[death_df["Country/Region"] == country]

    nc_data = nepal_cases.iloc[:, 4:]
    nr_data = nepal_recovered.iloc[:, 4:]
    nd_data = nepal_death.iloc[:, 4:]

    df3 = pd.concat([nc_data, nr_data, nd_data], ignore_index=True)

    return df3


def get_countires():
    confirmed_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    )
    pdToList = list(confirmed_df["Country/Region"])
    new_line = sorted(set(pdToList), key=pdToList.index)

    return new_line


def get_summary(country):
    country_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
    )
    cou = country_df.loc[country_df["Country_Region"] == country]
    summary = cou.iloc[0].tolist()
    return summary


def country_wise_summary(country):
    country_df = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
    )
    detail = country_df.loc[country_df["Country_Region"] == country]

    return detail


def nepal_stats():
    url = "https://nepalcorona.info/api/v1/data/nepal"
    response = requests.get(url)
    todos = json.loads(response.text)

    return todos


#  provience wise data onf test quaratine , rdt , appendnd isolatio
def provience_test_all(provience):
    rdt = pd.read_csv(
        "https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/site-report-mohp%20-%20rdttest.csv"
    )
    isolation = pd.read_csv(
        "https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/site-report-mohp%20-%20isolation.csv"
    )
    quaratine = pd.read_csv(
        "https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/site-report-mohp%20-%20quarantine.csv"
    )

    r = rdt.iloc[:, -1]
    i = isolation.iloc[:, -1]
    q = quaratine.iloc[:, -1]
    if provience == 8:
        ret = [r.sum(), q.sum(), i.sum(), isolation.columns[-1]]
    else:
        ret = [r[provience], q[provience], i[provience], isolation.columns[-1]]

    return ret


# provience wise summaray of test, cases, deaths and recovered.
def nepal_allprovience_stats(code):
    rdt = pd.read_csv(
        "https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/site-report-mohp%20-%20rdttest.csv"
    )
    isolation = pd.read_csv(
        "https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/site-report-mohp%20-%20isolation.csv"
    )
    quaratine = pd.read_csv(
        "https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/site-report-mohp%20-%20quarantine.csv"
    )

    r = rdt.iloc[:, -1]
    i = isolation.iloc[:, -1]
    q = quaratine.iloc[:, -1]

    df = pd.concat([r, i, q], axis=1, sort=False)

    return df


def get_ac_re_type(code):
    covid_df = create_covid_df()
    covid_df_active = pd.DataFrame(columns=covid_df.columns)
    covid_df_recovered = pd.DataFrame(columns=covid_df.columns)
    for i in range(len(covid_df)):
        data = pd.Series(covid_df.iloc[i, :])
        if covid_df.iloc[i]["currentstate"] == "active":
            covid_df_active = covid_df_active.append(data, ignore_index=True)
        else:
            covid_df_recovered = covid_df_recovered.append(data, ignore_index=True)

    covid_df_active["Active Cases"] = covid_df_active.groupby([code])[code].transform(
        "count"
    )
    covid_df_active = covid_df_active.drop_duplicates(code)
    #     print(covid_df_active[[code,'Active Cases']])

    covid_df_recovered["Recovered Cases"] = covid_df_recovered.groupby([code])[
        code
    ].transform("count")
    covid_df_recovered = covid_df_recovered.drop_duplicates(code)
    #     print(covid_df_recovered[[code, "Recovered Cases"]])

    covid_ac_re = pd.DataFrame()
    #     print(covid_df_active)
    covid_df_active_mod = covid_df_active[[code, "Active Cases"]]
    covid_df_recovered_mod = covid_df_recovered[[code, "Recovered Cases"]]

    covid_ac_re = covid_df_active_mod.merge(
        covid_df_recovered_mod, on=[code], how="outer"
    )

    covid_ac_re["Active Cases"] = covid_ac_re["Active Cases"].fillna(0)
    covid_ac_re["Recovered Cases"] = covid_ac_re["Recovered Cases"].fillna(0)

    return covid_ac_re.sort_values(by=["Active Cases"])


def provience_ac_re(provience):
    df = create_covid_df()
    abr = df[(df["provience"] == provience) & (df["currentstate"] == "recovered")]
    aba = df[(df["provience"] == provience) & (df["currentstate"] == "active")]
    acre = [len(aba), len(abr)]
    return acre


def provience_ma_fe(provience):
    df = create_covid_df()
    abm = df[(df["provience"] == provience) & (df["gender"] == "male")]
    abf = df[(df["provience"] == provience) & (df["gender"] == "female")]
    mafe = [len(abm), len(abf)]
    return mafe

