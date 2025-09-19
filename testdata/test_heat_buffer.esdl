<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="course_model with return network" id="3b21ab49-fd94-4dda-878d-dcaf651ded78_with_return_network" description="basic" esdlVersion="v2111" version="11">
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
        <port xsi:type="esdl:InPort" id="c3eb59bc-037d-4684-918e-df0f54af5b3d" name="In" connectedTo="9e1c58ab-ec19-4964-928f-d2a582af6ce8" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="131d801f-9f8e-4dc4-9a8a-82725607eedf" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand2_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="fcf96c55-8264-41a5-90ee-0977a394a46a" name="Out" connectedTo="99628a79-e31c-4a99-bf4a-2f788a5d5343" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" name="Delfgauw" id="8805731a-8780-47b4-8204-76ba074564bc" minTemperature="40.0" maxTemperature="120.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.0094006941874" lon="4.396162033081056"/>
        <port xsi:type="esdl:InPort" id="69464799-3ec3-4928-a5da-6158a6237c76" name="In" connectedTo="88b6c35c-7eeb-42e9-ba4e-491fa6c7a6fc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="0380fe5a-611c-4523-9eda-1d0ecd69271e" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand1_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="c8625b7f-e9ad-4327-899e-0c6e91e873cb" name="Out" connectedTo="1467bee7-ed90-49d5-8395-3595408ad1ee" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" name="Nootdorp" id="156c4afb-4106-4286-8f41-fbf8edc6e5ce" minTemperature="40.0" maxTemperature="120.0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.04277777849674" lon="4.3912696838378915"/>
        <port xsi:type="esdl:InPort" id="ad377fa7-710f-45e7-9144-1521bef5c1ab" name="In" connectedTo="22be2ae1-10c0-42eb-abd9-6b115b800283" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret">
          <profile xsi:type="esdl:InfluxDBProfile" multiplier="5.0" startDate="2018-12-31T23:00:00.000000+0000" filters="" id="57131b4a-f177-47da-b7d7-788f23eefb5b" measurement="WarmingUp default profiles" database="energy_profiles" host="profiles.warmingup.info" port="443" field="demand3_MW" endDate="2019-12-31T22:00:00.000000+0000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="f46090b9-dcd6-433f-b021-061c839e634c" name="Out" connectedTo="fdbab763-3e05-49d6-9271-207035c14bcb" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_1126" id="11262f35-3d51-4ce3-9a69-6eb4a6c46c9d">
        <geometry xsi:type="esdl:Point" lon="4.401419162750245" lat="52.01909093233181" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="a8779f8a-3d61-4a97-bfb4-35029175ec97" name="In" connectedTo="7c178a7c-f6cb-4f33-8c4a-076d9131ed8a" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="fd562e07-a60c-4f5c-9084-d51e736ff545" name="Out" connectedTo="a89b5045-f815-4126-a4c8-dc125a99c0f8 b9af6540-8cae-41ce-b0c3-4528e027d3b3" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN80" name="Pipe1" innerDiameter="0.08" length="1533.2" id="Pipe1" outerDiameter="0.09" related="Pipe1_ret">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.01909093233181" lon="4.401419162750245"/>
          <point xsi:type="esdl:Point" lat="52.01563438289948" lon="4.391613006591798"/>
          <point xsi:type="esdl:Point" lat="52.0094006941874" lon="4.396162033081056"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="a89b5045-f815-4126-a4c8-dc125a99c0f8" name="In" connectedTo="fd562e07-a60c-4f5c-9084-d51e736ff545" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="88b6c35c-7eeb-42e9-ba4e-491fa6c7a6fc" name="Out" connectedTo="69464799-3ec3-4928-a5da-6158a6237c76" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN200" name="Pipe2" innerDiameter="0.2" length="44.4" id="Pipe2" outerDiameter="0.21" related="Pipe2_ret">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.019437562955694" lon="4.401097297668458"/>
          <point xsi:type="esdl:Point" lat="52.01909093233181" lon="4.401419162750245"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="30f746ff-aca7-4e55-946e-3dcaf2ac7569" name="In" connectedTo="7dde77c4-a956-4496-b8b9-e714317cc0f2" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="7c178a7c-f6cb-4f33-8c4a-076d9131ed8a" name="Out" connectedTo="a8779f8a-3d61-4a97-bfb4-35029175ec97" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_91b0" id="91b0e057-84cd-4db3-8d2d-cae02077cbaf">
        <geometry xsi:type="esdl:Point" lon="4.422471821308137" lat="52.02578372981452" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="6829cf4d-0dd9-43ac-8581-87b9998ca5bc" name="In" connectedTo="607e9ed3-3e2e-4c08-bffe-0d713420cce7" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="416291d2-c5f7-4a87-919a-655924b90eb2" name="Out" connectedTo="e3b7d0a5-e7d7-4cb2-8a33-e56d2077616b 758212e1-ab7f-44b1-a203-6ed42eb3c6bc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN100" name="Pipe3" innerDiameter="0.1" length="1157.3" id="Pipe3" outerDiameter="0.11" related="Pipe3_ret">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.02578372981452" lon="4.422471821308137"/>
          <point xsi:type="esdl:Point" lat="52.02318760445455" lon="4.425044059753419"/>
          <point xsi:type="esdl:Point" lat="52.02034869350056" lon="4.4269752502441415"/>
          <point xsi:type="esdl:Point" lat="52.018381156483095" lon="4.428133964538575"/>
          <point xsi:type="esdl:Point" lat="52.01906782352804" lon="4.431524276733399"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e3b7d0a5-e7d7-4cb2-8a33-e56d2077616b" name="In" connectedTo="416291d2-c5f7-4a87-919a-655924b90eb2" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="9e1c58ab-ec19-4964-928f-d2a582af6ce8" name="Out" connectedTo="c3eb59bc-037d-4684-918e-df0f54af5b3d" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN100" name="Pipe4" innerDiameter="0.1" length="2982.2" id="Pipe4" outerDiameter="0.11" related="Pipe4_ret">
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
        <port xsi:type="esdl:InPort" id="758212e1-ab7f-44b1-a203-6ed42eb3c6bc" name="In" connectedTo="416291d2-c5f7-4a87-919a-655924b90eb2" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="22be2ae1-10c0-42eb-abd9-6b115b800283" name="Out" connectedTo="ad377fa7-710f-45e7-9144-1521bef5c1ab" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_1126_ret" id="c6fec31e-2c4a-423d-937c-7fc28ea81a21">
        <geometry xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="c06f582d-1922-47e3-ae04-a740b28353e3" name="ret_port" connectedTo="b4a30d86-df7a-4136-9170-55087818800d 35ff6c51-ecdc-419c-9e67-8dbbf4ccaa42" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="39c08ebb-b7d8-4a85-a226-800c225a8a61" name="ret_port" connectedTo="fb153d7c-2dc3-4f53-bbee-f0060efef1c7" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_91b0_ret" id="b7a46b09-779f-4a57-b73e-ab707ec65842">
        <geometry xsi:type="esdl:Point" lon="4.421796245126029" lat="52.02587372990452" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="9a5c2e7e-e970-4561-8538-9a4000dee416" name="ret_port" connectedTo="002a5802-e55b-4025-abe9-8d508cfdd78c 0c142bfb-4b38-44aa-b88f-71da247525ef" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="3383078a-72da-4af1-badf-686f43c73018" name="ret_port" connectedTo="bbb482fa-f98e-4219-ab7e-d8684b0b4e66" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN80" name="Pipe1_ret" innerDiameter="0.08" length="1533.2" id="Pipe1_ret" outerDiameter="0.09" related="Pipe1">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.3954232586139" lat="52.009490694277396" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.3908996472617385" lat="52.015724382989475" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="1467bee7-ed90-49d5-8395-3595408ad1ee" name="In_ret" connectedTo="c8625b7f-e9ad-4327-899e-0c6e91e873cb" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="b4a30d86-df7a-4136-9170-55087818800d" name="Out_ret" connectedTo="c06f582d-1922-47e3-ae04-a740b28353e3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN200" name="Pipe2_ret" innerDiameter="0.2" length="44.4" id="Pipe2_ret" outerDiameter="0.21" related="Pipe2">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400398589922203" lat="52.01952756304569" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="fb153d7c-2dc3-4f53-bbee-f0060efef1c7" name="In_ret" connectedTo="39c08ebb-b7d8-4a85-a226-800c225a8a61" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="095f2c36-395f-4183-a760-80d5362e1de3" name="Out_ret" connectedTo="f8113571-6167-4850-b558-f97f39a0a3f3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN100" name="Pipe3_ret" innerDiameter="0.1" length="1157.3" id="Pipe3_ret" outerDiameter="0.11" related="Pipe3">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.4308241714884975" lat="52.01915782361804" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.427431248765651" lat="52.01847115657309" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.426279962182911" lat="52.020438693590556" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.42435921177036" lat="52.023277604544546" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.421796245126029" lat="52.02587372990452" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="99628a79-e31c-4a99-bf4a-2f788a5d5343" name="In_ret" connectedTo="fcf96c55-8264-41a5-90ee-0977a394a46a" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="002a5802-e55b-4025-abe9-8d508cfdd78c" name="Out_ret" connectedTo="9a5c2e7e-e970-4561-8538-9a4000dee416" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN100" name="Pipe4_ret" innerDiameter="0.1" length="2982.2" id="Pipe4_ret" outerDiameter="0.11" related="Pipe4">
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
        <port xsi:type="esdl:InPort" id="fdbab763-3e05-49d6-9271-207035c14bcb" name="In_ret" connectedTo="f46090b9-dcd6-433f-b021-061c839e634c" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="0c142bfb-4b38-44aa-b88f-71da247525ef" name="Out_ret" connectedTo="9a5c2e7e-e970-4561-8538-9a4000dee416" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN150" name="Pipe5_a" innerDiameter="0.15" length="625.29" id="2b5ba02c-bbfe-4bb9-9e4e-48c4c45c53e9" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.01909093233181" lon="4.401419162750245"/>
          <point xsi:type="esdl:Point" lat="52.02149748382286" lon="4.408371448516847"/>
          <point xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="b9af6540-8cae-41ce-b0c3-4528e027d3b3" name="In" connectedTo="fd562e07-a60c-4f5c-9084-d51e736ff545" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="37a4d419-e788-4ca7-a033-3a06c6872fdf" name="Out" connectedTo="9b3744f2-f9f0-4e32-a118-e116154e1384" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN150" name="Pipe5_b" innerDiameter="0.15" length="999.47" id="0f7eed4a-ac9a-4f38-9825-876e41e8c100" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
          <point xsi:type="esdl:Point" lat="52.0233064386584" lon="4.414680004119874"/>
          <point xsi:type="esdl:Point" lat="52.025085613014795" lon="4.419805705547334"/>
          <point xsi:type="esdl:Point" lat="52.02567150373549" lon="4.421594738960267"/>
          <point xsi:type="esdl:Point" lat="52.02578372981452" lon="4.422471821308137"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="9a462e32-2e53-40ca-97eb-8394b6a3d131" name="In" connectedTo="3a52317d-827b-4dc4-a6df-1b145bbb1736" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="607e9ed3-3e2e-4c08-bffe-0d713420cce7" name="Out" connectedTo="6829cf4d-0dd9-43ac-8581-87b9998ca5bc" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_086f" id="086f467d-afd5-4a87-aad2-0b03f185edef">
        <geometry xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
        <port xsi:type="esdl:InPort" id="9b3744f2-f9f0-4e32-a118-e116154e1384" name="In" connectedTo="37a4d419-e788-4ca7-a033-3a06c6872fdf" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="3a52317d-827b-4dc4-a6df-1b145bbb1736" name="Out" connectedTo="9a462e32-2e53-40ca-97eb-8394b6a3d131 3874047c-96e8-4555-902a-8646daf3f984" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN150" name="Pipe5_ret_a" innerDiameter="0.1" length="993.35" id="3a1d7c9a-18cd-4360-ae7f-74062a514317" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.02587372990452" lon="4.421796245126029"/>
          <point xsi:type="esdl:Point" lon="4.420918767262569" lat="52.025761503825485" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.419127661327588" lat="52.02517561310479" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.413995586196941" lat="52.0233964387484" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lat="52.021920019967986" lon="4.4088220596313485"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="bbb482fa-f98e-4219-ab7e-d8684b0b4e66" name="In_ret" connectedTo="3383078a-72da-4af1-badf-686f43c73018" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="23be2b8d-5f5a-471f-875f-b7e20997f7c5" name="Out" connectedTo="027db45e-289d-4611-94ba-95d04abec30f" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN150" name="Pipe5_ret_b" innerDiameter="0.1" length="632.79" id="92af5656-dbd3-4ddf-abaa-9ef47ea96333" outerDiameter="0.16">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.021920019967986" lon="4.4088220596313485"/>
          <point xsi:type="esdl:Point" lon="4.4076804239030505" lat="52.02158748391286" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.400719145015912" lat="52.019180932421804" CRS="WGS84"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="fb200deb-6383-4e50-b041-9536046ee404" name="In" connectedTo="ba8ac663-b53c-400a-a838-206da20b63d7" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="35ff6c51-ecdc-419c-9e67-8dbbf4ccaa42" name="Out_ret" connectedTo="c06f582d-1922-47e3-ae04-a740b28353e3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_526a" id="526a38b8-cf6c-407e-9a76-837d409fdf12">
        <geometry xsi:type="esdl:Point" lat="52.021920019967986" lon="4.4088220596313485"/>
        <port xsi:type="esdl:InPort" id="027db45e-289d-4611-94ba-95d04abec30f" name="In" connectedTo="23be2b8d-5f5a-471f-875f-b7e20997f7c5 7ca06d72-bb1d-41ac-9a19-6306fb33e10e" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="ba8ac663-b53c-400a-a838-206da20b63d7" name="Out" connectedTo="fb200deb-6383-4e50-b041-9536046ee404" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN150" name="Pipe_ates" length="599.3" id="fa07b73b-0ec7-4a6d-bbd5-60b5fdf09d92">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.021827590527295" lon="4.409401416778565"/>
          <point xsi:type="esdl:Point" lat="52.02648843713918" lon="4.4050025939941415"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3874047c-96e8-4555-902a-8646daf3f984" name="In" connectedTo="3a52317d-827b-4dc4-a6df-1b145bbb1736" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="b94d1e9b-5377-4016-9bb3-4452effb5a20" name="Out" connectedTo="58fa3db6-c1e6-4c8c-b540-1e17985b79d5" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" diameter="DN150" name="Pipe_ates_ret" length="549.0" id="1f1a7ed1-c6fe-4afe-a39c-77803b8aed2f">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.02633000273639" lon="4.404745101928712"/>
          <point xsi:type="esdl:Point" lat="52.02203885753961" lon="4.408714771270753"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="9a58c5ba-1ac1-48cb-b583-5c568190ae3c" name="In" connectedTo="93f83b88-bb0b-4a83-bad7-713530347380" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
        <port xsi:type="esdl:OutPort" id="7ca06d72-bb1d-41ac-9a19-6306fb33e10e" name="Out" connectedTo="027db45e-289d-4611-94ba-95d04abec30f" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" power="100000000.0" name="GenericProducer_0375" id="0375b489-b57b-439d-9ce9-db2dc9d0bbb9">
        <geometry xsi:type="esdl:Point" lon="4.40077438452907" CRS="WGS84" lat="52.0197014548679"/>
        <port xsi:type="esdl:OutPort" id="7dde77c4-a956-4496-b8b9-e714317cc0f2" name="Out" connectedTo="30f746ff-aca7-4e55-946e-3dcaf2ac7569" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:InPort" id="f8113571-6167-4850-b558-f97f39a0a3f3" name="In" connectedTo="095f2c36-395f-4183-a760-80d5362e1de3" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
      <asset xsi:type="esdl:HeatStorage" id="7ce0ddec-890b-4abb-99d8-2fd6666d02f6" name="HeatStorage_7ce0" maxChargeRate="1000000.0" maxDischargeRate="1000000.0" volume="50.0">
        <geometry xsi:type="esdl:Point" lat="52.026718233499246" lon="4.4045103755280754" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="58fa3db6-c1e6-4c8c-b540-1e17985b79d5" name="In" connectedTo="b94d1e9b-5377-4016-9bb3-4452effb5a20" carrier="e96c4852-b2bc-43be-8fa7-5ae5e25a1883_ret"/>
        <port xsi:type="esdl:OutPort" id="93f83b88-bb0b-4a83-bad7-713530347380" name="Out" connectedTo="9a58c5ba-1ac1-48cb-b583-5c568190ae3c" carrier="bac202fe-7c5f-4623-8ade-badbc607a16e_ret"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
