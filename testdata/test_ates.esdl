<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="course_model with return network" id="3b21ab49-fd94-4dda-878d-dcaf651ded78_with_return_network" description="basic" esdlVersion="v2111" version="10">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="9a76b800-6e2c-4e99-a9a5-859f7badd061">
    <carriers xsi:type="esdl:Carriers" id="e84423d9-b617-4fa0-b113-1ba12daacaaf">
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" id="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="supply_ret" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" id="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Return_ret" supplyTemperature="80.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="54fda8fc-e725-4c44-8a49-726a811ba069">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="eb07bccb-203f-407e-af98-e687656a221d" description="Energy in GJ" multiplier="GIGA" physicalQuantity="ENERGY" unit="JOULE"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" multiplier="MEGA" physicalQuantity="POWER" unit="WATT"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1a" description="Power in kW" multiplier="KILO" physicalQuantity="POWER" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="8db3337e-440e-48d1-b1e9-6f86c4f76320" name="Untitled instance">
    <area xsi:type="esdl:Area" id="a3f3b5d9-2faa-4862-a5b0-d02b219052dd" name="Untitled area">
      <asset xsi:type="esdl:HeatingDemand" name="Pijnacker" id="cc61c52a-29a6-45d3-81e8-ce18ba12f319" minTemperature="40.0" maxTemperature="120.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.01906782352804" lon="4.431524276733399"/>
        <port xsi:type="esdl:InPort" connectedTo="9e1c58ab-ec19-4964-928f-d2a582af6ce8" id="c3eb59bc-037d-4684-918e-df0f54af5b3d" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="131d801f-9f8e-4dc4-9a8a-82725607eedf" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand2_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="fcf96c55-8264-41a5-90ee-0977a394a46a" connectedTo="99628a79-e31c-4a99-bf4a-2f788a5d5343" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" name="Delfgauw" id="8805731a-8780-47b4-8204-76ba074564bc" minTemperature="40.0" maxTemperature="120.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.0094006941874" lon="4.396162033081056"/>
        <port xsi:type="esdl:InPort" connectedTo="88b6c35c-7eeb-42e9-ba4e-491fa6c7a6fc" id="69464799-3ec3-4928-a5da-6158a6237c76" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="0380fe5a-611c-4523-9eda-1d0ecd69271e" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand1_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="c8625b7f-e9ad-4327-899e-0c6e91e873cb" connectedTo="1467bee7-ed90-49d5-8395-3595408ad1ee" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" name="Nootdorp" id="156c4afb-4106-4286-8f41-fbf8edc6e5ce" minTemperature="40.0" maxTemperature="120.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.04277777849674" lon="4.3912696838378915"/>
        <port xsi:type="esdl:InPort" connectedTo="22be2ae1-10c0-42eb-abd9-6b115b800283" id="ad377fa7-710f-45e7-9144-1521bef5c1ab" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="57131b4a-f177-47da-b7d7-788f23eefb5b" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand3_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="f46090b9-dcd6-433f-b021-061c839e634c" connectedTo="fdbab763-3e05-49d6-9271-207035c14bcb" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_1126" id="11262f35-3d51-4ce3-9a69-6eb4a6c46c9d">
        <geometry xsi:type="esdl:Point" lon="4.401419162750245" lat="52.01909093233181" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" connectedTo="7c178a7c-f6cb-4f33-8c4a-076d9131ed8a" id="a8779f8a-3d61-4a97-bfb4-35029175ec97" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="fd562e07-a60c-4f5c-9084-d51e736ff545" connectedTo="a89b5045-f815-4126-a4c8-dc125a99c0f8 b9af6540-8cae-41ce-b0c3-4528e027d3b3" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe1_ret" name="Pipe1" innerDiameter="0.08" length="1533.2" id="Pipe1" outerDiameter="0.09">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.01909093233181" lon="4.401419162750245"/>
          <point xsi:type="esdl:Point" lat="52.01563438289948" lon="4.391613006591798"/>
          <point xsi:type="esdl:Point" lat="52.0094006941874" lon="4.396162033081056"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="fd562e07-a60c-4f5c-9084-d51e736ff545" id="a89b5045-f815-4126-a4c8-dc125a99c0f8" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="88b6c35c-7eeb-42e9-ba4e-491fa6c7a6fc" connectedTo="69464799-3ec3-4928-a5da-6158a6237c76" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe2_ret" name="Pipe2" innerDiameter="0.2" length="44.4" id="Pipe2" outerDiameter="0.21">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.019437562955694" lon="4.401097297668458"/>
          <point xsi:type="esdl:Point" lat="52.01909093233181" lon="4.401419162750245"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="7dde77c4-a956-4496-b8b9-e714317cc0f2" id="30f746ff-aca7-4e55-946e-3dcaf2ac7569" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="7c178a7c-f6cb-4f33-8c4a-076d9131ed8a" connectedTo="a8779f8a-3d61-4a97-bfb4-35029175ec97" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_91b0" id="91b0e057-84cd-4db3-8d2d-cae02077cbaf">
        <geometry xsi:type="esdl:Point" lon="4.422471821308137" lat="52.02578372981452" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" connectedTo="607e9ed3-3e2e-4c08-bffe-0d713420cce7" id="6829cf4d-0dd9-43ac-8581-87b9998ca5bc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="416291d2-c5f7-4a87-919a-655924b90eb2" connectedTo="e3b7d0a5-e7d7-4cb2-8a33-e56d2077616b 758212e1-ab7f-44b1-a203-6ed42eb3c6bc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe3_ret" name="Pipe3" innerDiameter="0.1" length="1157.3" id="Pipe3" outerDiameter="0.11">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.02578372981452" lon="4.422471821308137"/>
          <point xsi:type="esdl:Point" lat="52.02318760445455" lon="4.425044059753419"/>
          <point xsi:type="esdl:Point" lat="52.02034869350056" lon="4.4269752502441415"/>
          <point xsi:type="esdl:Point" lat="52.018381156483095" lon="4.428133964538575"/>
          <point xsi:type="esdl:Point" lat="52.01906782352804" lon="4.431524276733399"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="416291d2-c5f7-4a87-919a-655924b90eb2" id="e3b7d0a5-e7d7-4cb2-8a33-e56d2077616b" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="9e1c58ab-ec19-4964-928f-d2a582af6ce8" connectedTo="c3eb59bc-037d-4684-918e-df0f54af5b3d" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe4_ret" name="Pipe4" innerDiameter="0.1" length="2982.2" id="Pipe4" outerDiameter="0.11">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.02578372981452" lon="4.422471821308137"/>
          <point xsi:type="esdl:Point" lat="52.030501921460775" lon="4.419465065002442"/>
          <point xsi:type="esdl:Point" lat="52.033379790423076" lon="4.416353702545167"/>
          <point xsi:type="esdl:Point" lat="52.035940674013524" lon="4.408607482910157"/>
          <point xsi:type="esdl:Point" lat="52.03683826859462" lon="4.405066967010499"/>
          <point xsi:type="esdl:Point" lat="52.03810543026395" lon="4.400925636291505"/>
          <point xsi:type="esdl:Point" lat="52.04211787192499" lon="4.393007755279542"/>
          <point xsi:type="esdl:Point" lat="52.04283057060157" lon="4.391098022460938"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="416291d2-c5f7-4a87-919a-655924b90eb2" id="758212e1-ab7f-44b1-a203-6ed42eb3c6bc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="22be2ae1-10c0-42eb-abd9-6b115b800283" connectedTo="ad377fa7-710f-45e7-9144-1521bef5c1ab" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_1126_ret" id="c6fec31e-2c4a-423d-937c-7fc28ea81a21">
        <geometry xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" connectedTo="b4a30d86-df7a-4136-9170-55087818800d 35ff6c51-ecdc-419c-9e67-8dbbf4ccaa42" id="c06f582d-1922-47e3-ae04-a740b28353e3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="ret_port"/>
        <port xsi:type="esdl:OutPort" id="39c08ebb-b7d8-4a85-a226-800c225a8a61" connectedTo="fb153d7c-2dc3-4f53-bbee-f0060efef1c7" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="ret_port"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_91b0_ret" id="b7a46b09-779f-4a57-b73e-ab707ec65842">
        <geometry xsi:type="esdl:Point" lon="4.421796245126029" lat="52.02587372990452" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" connectedTo="002a5802-e55b-4025-abe9-8d508cfdd78c 0c142bfb-4b38-44aa-b88f-71da247525ef" id="9a5c2e7e-e970-4561-8538-9a4000dee416" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="ret_port"/>
        <port xsi:type="esdl:OutPort" id="3383078a-72da-4af1-badf-686f43c73018" connectedTo="bbb482fa-f98e-4219-ab7e-d8684b0b4e66" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="ret_port"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe1" name="Pipe1_ret" innerDiameter="0.08" length="1533.2" id="Pipe1_ret" outerDiameter="0.09">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.3954232586139" lat="52.009490694277396" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.3908996472617385" lat="52.015724382989475" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="c8625b7f-e9ad-4327-899e-0c6e91e873cb" id="1467bee7-ed90-49d5-8395-3595408ad1ee" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In_ret"/>
        <port xsi:type="esdl:OutPort" id="b4a30d86-df7a-4136-9170-55087818800d" connectedTo="c06f582d-1922-47e3-ae04-a740b28353e3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe2" name="Pipe2_ret" innerDiameter="0.2" length="44.4" id="Pipe2_ret" outerDiameter="0.21">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400398589922203" lat="52.01952756304569" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="39c08ebb-b7d8-4a85-a226-800c225a8a61" id="fb153d7c-2dc3-4f53-bbee-f0060efef1c7" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In_ret"/>
        <port xsi:type="esdl:OutPort" id="095f2c36-395f-4183-a760-80d5362e1de3" connectedTo="f8113571-6167-4850-b558-f97f39a0a3f3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe3" name="Pipe3_ret" innerDiameter="0.1" length="1157.3" id="Pipe3_ret" outerDiameter="0.11">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.4308241714884975" lat="52.01915782361804" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.427431248765651" lat="52.01847115657309" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.426279962182911" lat="52.020438693590556" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.42435921177036" lat="52.023277604544546" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.421796245126029" lat="52.02587372990452" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="fcf96c55-8264-41a5-90ee-0977a394a46a" id="99628a79-e31c-4a99-bf4a-2f788a5d5343" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In_ret"/>
        <port xsi:type="esdl:OutPort" id="002a5802-e55b-4025-abe9-8d508cfdd78c" connectedTo="9a5c2e7e-e970-4561-8538-9a4000dee416" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe4" name="Pipe4_ret" innerDiameter="0.1" length="2982.2" id="Pipe4_ret" outerDiameter="0.11">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.390477502296783" lat="52.04292057069157" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.392385117209615" lat="52.042207872014984" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400290793359585" lat="52.038195430353944" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.404428167491401" lat="52.03692826868462" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.407965850141681" lat="52.03603067410352" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.41570384355307" lat="52.033469790513074" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.418805700922162" lat="52.03059192155077" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.421796245126029" lat="52.02587372990452" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="f46090b9-dcd6-433f-b021-061c839e634c" id="fdbab763-3e05-49d6-9271-207035c14bcb" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In_ret"/>
        <port xsi:type="esdl:OutPort" id="0c142bfb-4b38-44aa-b88f-71da247525ef" connectedTo="9a5c2e7e-e970-4561-8538-9a4000dee416" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe5_a" innerDiameter="0.15" length="625.29" id="2b5ba02c-bbfe-4bb9-9e4e-48c4c45c53e9" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.01909093233181" lon="4.401419162750245"/>
          <point xsi:type="esdl:Point" lat="52.02149748382286" lon="4.408371448516847"/>
          <point xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="fd562e07-a60c-4f5c-9084-d51e736ff545" id="b9af6540-8cae-41ce-b0c3-4528e027d3b3" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="37a4d419-e788-4ca7-a033-3a06c6872fdf" connectedTo="9b3744f2-f9f0-4e32-a118-e116154e1384" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe5_b" innerDiameter="0.15" length="999.47" id="0f7eed4a-ac9a-4f38-9825-876e41e8c100" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
          <point xsi:type="esdl:Point" lat="52.0233064386584" lon="4.414680004119874"/>
          <point xsi:type="esdl:Point" lat="52.025085613014795" lon="4.419805705547334"/>
          <point xsi:type="esdl:Point" lat="52.02567150373549" lon="4.421594738960267"/>
          <point xsi:type="esdl:Point" lat="52.02578372981452" lon="4.422471821308137"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="3a52317d-827b-4dc4-a6df-1b145bbb1736" id="9a462e32-2e53-40ca-97eb-8394b6a3d131" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="607e9ed3-3e2e-4c08-bffe-0d713420cce7" connectedTo="6829cf4d-0dd9-43ac-8581-87b9998ca5bc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_086f" id="086f467d-afd5-4a87-aad2-0b03f185edef">
        <geometry xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
        <port xsi:type="esdl:InPort" connectedTo="37a4d419-e788-4ca7-a033-3a06c6872fdf" id="9b3744f2-f9f0-4e32-a118-e116154e1384" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="3a52317d-827b-4dc4-a6df-1b145bbb1736" connectedTo="9a462e32-2e53-40ca-97eb-8394b6a3d131 3874047c-96e8-4555-902a-8646daf3f984" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe5_ret_a" innerDiameter="0.1" length="993.35" id="3a1d7c9a-18cd-4360-ae7f-74062a514317" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.02587372990452" lon="4.421796245126029"/>
          <point xsi:type="esdl:Point" lon="4.420918767262569" lat="52.025761503825485" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.419127661327588" lat="52.02517561310479" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.413995586196941" lat="52.0233964387484" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lat="52.021920019967986" lon="4.4088220596313485"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="3383078a-72da-4af1-badf-686f43c73018" id="bbb482fa-f98e-4219-ab7e-d8684b0b4e66" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In_ret"/>
        <port xsi:type="esdl:OutPort" id="23be2b8d-5f5a-471f-875f-b7e20997f7c5" connectedTo="027db45e-289d-4611-94ba-95d04abec30f" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe5_ret_b" innerDiameter="0.1" length="632.79" id="92af5656-dbd3-4ddf-abaa-9ef47ea96333" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.021920019967986" lon="4.4088220596313485"/>
          <point xsi:type="esdl:Point" lon="4.4076804239030505" lat="52.02158748391286" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="ba8ac663-b53c-400a-a838-206da20b63d7" id="fb200deb-6383-4e50-b041-9536046ee404" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="35ff6c51-ecdc-419c-9e67-8dbbf4ccaa42" connectedTo="c06f582d-1922-47e3-ae04-a740b28353e3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_526a" id="526a38b8-cf6c-407e-9a76-837d409fdf12">
        <geometry xsi:type="esdl:Point" lat="52.021920019967986" lon="4.4088220596313485"/>
        <port xsi:type="esdl:InPort" connectedTo="23be2b8d-5f5a-471f-875f-b7e20997f7c5 7ca06d72-bb1d-41ac-9a19-6306fb33e10e" id="027db45e-289d-4611-94ba-95d04abec30f" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="ba8ac663-b53c-400a-a838-206da20b63d7" connectedTo="fb200deb-6383-4e50-b041-9536046ee404" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_ates" length="599.3" id="fa07b73b-0ec7-4a6d-bbd5-60b5fdf09d92">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
          <point xsi:type="esdl:Point" lat="52.02648843713918" lon="4.4050025939941415"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="3a52317d-827b-4dc4-a6df-1b145bbb1736" id="3874047c-96e8-4555-902a-8646daf3f984" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="b94d1e9b-5377-4016-9bb3-4452effb5a20" connectedTo="e14c67db-96c3-4fc9-aed2-4fe0f84a34d3" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:Pipe" name="Pipe_ates_ret" length="549.0" id="1f1a7ed1-c6fe-4afe-a39c-77803b8aed2f">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.02633000273639" lon="4.404745101928712"/>
          <point xsi:type="esdl:Point" lat="52.02203885753961" lon="4.408714771270753"/>
        </geometry>
        <port xsi:type="esdl:InPort" connectedTo="07a302f6-4e5b-40ef-87e3-c908a993dfe4" id="9a58c5ba-1ac1-48cb-b583-5c568190ae3c" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In"/>
        <port xsi:type="esdl:OutPort" id="7ca06d72-bb1d-41ac-9a19-6306fb33e10e" connectedTo="027db45e-289d-4611-94ba-95d04abec30f" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
      </asset>
      <asset xsi:type="esdl:ATES" aquiferNetToGross="1.0" name="ATES_4d6d" aquiferThickness="45.0" maxDischargeRate="11610000.0" wellCasingSize="13.0" aquiferAnisotropy="4.0" aquiferPorosity="0.3" aquiferTopDepth="300.0" aquiferMidTemperature="17.0" id="4d6dfb40-ea51-4176-a27e-4ee60cad4034" wellDistance="150.0" maxChargeRate="11610000.0" salinity="10000.0" aquiferPermeability="10000.0">
        <geometry xsi:type="esdl:Point" lat="52.026597360465495" lon="4.404745101928712"/>
        <dataSource xsi:type="esdl:DataSource" description="This data was generated using the 'kosten_per_asset.xslx' file in the 'Kentallen' directory of WarmingUp project 1D" attribution="" name="WarmingUp factsheet: HT-ATES (high)"/>
        <port xsi:type="esdl:InPort" connectedTo="b94d1e9b-5377-4016-9bb3-4452effb5a20" id="e14c67db-96c3-4fc9-aed2-4fe0f84a34d3" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="In">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="1e323c5f-f645-42bf-8631-b63b0a24c424" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand4_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="07a302f6-4e5b-40ef-87e3-c908a993dfe4" connectedTo="9a58c5ba-1ac1-48cb-b583-5c568190ae3c" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="Out"/>
        <costInformation xsi:type="esdl:CostInformation">
          <fixedOperationalCosts xsi:type="esdl:SingleValue" value="30000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" perTimeUnit="YEAR" id="574ef21d-681a-43ae-a1cb-f7b25d88defb" description="Cost in EUR/yr"/>
          </fixedOperationalCosts>
          <variableOperationalCosts xsi:type="esdl:SingleValue" value="69666.67">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" perTimeUnit="YEAR" id="3c9f580e-b71a-4bc8-8cea-cb6788c0bf49" description="Cost in EUR/yr"/>
          </variableOperationalCosts>
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" value="115472.22">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" perTimeUnit="YEAR" id="57537388-7fd7-40b3-a0c4-0ce65648eaab" description="Cost in EUR/yr"/>
          </fixedMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" value="2333594.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" unit="EURO" id="a3b5cdd9-364b-4262-bce5-4658c5f1bac9" description="Cost in EUR"/>
          </investmentCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:GenericProducer" power="100000000.0" name="GenericProducer_0375" id="0375b489-b57b-439d-9ce9-db2dc9d0bbb9">
        <geometry xsi:type="esdl:Point" lon="4.40077438452907" CRS="WGS84" lat="52.0197014548679"/>
        <port xsi:type="esdl:OutPort" id="7dde77c4-a956-4496-b8b9-e714317cc0f2" connectedTo="30f746ff-aca7-4e55-946e-3dcaf2ac7569" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret" name="Out"/>
        <port xsi:type="esdl:InPort" connectedTo="095f2c36-395f-4183-a760-80d5362e1de3" id="f8113571-6167-4850-b558-f97f39a0a3f3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret" name="In"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
