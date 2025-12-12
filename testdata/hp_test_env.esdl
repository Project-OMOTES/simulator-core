<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="fdbbf5ee-6e86-4c82-9926-4b59de482378_with_return_network" description="" esdlVersion="v2207" name="Untitled EnergySystem with return network" version="7">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="c615f17e-c077-48c4-8a78-6ae05f8a908f">
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="f61a1799-bf04-416a-b15e-93097722ada7">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" multiplier="MEGA" unit="WATT" description="Power in MW"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" id="12c481c0-f81e-49b6-9767-90457684d24a" multiplier="KILO" unit="WATTHOUR" description="Energy in kWh"/>
    </quantityAndUnits>
    <carriers xsi:type="esdl:Carriers" id="c27258b1-f4f6-4e09-a77a-ce466dbd82d2">
      <carrier xsi:type="esdl:HeatCommodity" supplyTemperature="80.0" name="HeatSupplyprim" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" name="HeatReturnprim" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
      <carrier xsi:type="esdl:HeatCommodity" id="2225db3f-a223-4144-97f6-553ba911d4d5" name="HeatSupplysec" supplyTemperature="70.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="36a55910-fbfb-4c4e-9db2-7000140b90f8" name="HeatReturnsec" supplyTemperature="30.0"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="a357cbbe-f277-42b1-8456-cbbadc8ceb2e" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="e4002c22-abd5-43f6-81a8-e6b5f960bfa5">
      <asset xsi:type="esdl:HeatingDemand" id="48f3e425-2143-4dcd-9101-c7e22559e82b" name="HeatingDemand_48f3">
        <port xsi:type="esdl:InPort" id="af0904f7-ba1f-4e79-9040-71e08041601b" name="In" connectedTo="52c2357a-d1af-46be-94dc-bd66bebc2503" carrier="2225db3f-a223-4144-97f6-553ba911d4d5"/>
        <port xsi:type="esdl:OutPort" id="e890f65f-80e7-46fa-8c52-5385324bf686" name="Out" carrier="36a55910-fbfb-4c4e-9db2-7000140b90f8" connectedTo="9deb1682-5f54-485b-b5c5-bcbeda372b35">
          <profile xsi:type="esdl:InfluxDBProfile" endDate="2019-12-31T22:00:00.000000+0000" id="b77e41bc-a5ca-4823-b467-09872f2b6772" port="443" host="profiles.warmingup.info" filters="" startDate="2018-12-31T23:00:00.000000+0000" database="energy_profiles" measurement="WarmingUp default profiles" field="demand4_MW">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="4.63726043701172" lat="52.158769628869045"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" power="5000000.0" id="cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4" name="GenericProducer_cf3d">
        <port xsi:type="esdl:InPort" id="9c258b9d-3149-4720-8931-f4bef1080ec1" name="In" connectedTo="24fa1f65-7f13-48fa-8bc3-49b6f511ba8e" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" name="Out" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" connectedTo="3ec4b989-4238-4d3c-8621-f1b60ec5e75c"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="4.558639526367188" lat="52.148869383489114"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="de92f241-c765-48de-917d-02c151d04bf7" name="HeatPump_de92">
        <geometry xsi:type="esdl:Point" lat="52.160878993818656" lon="4.591542570956944" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="4ce16061-1b4e-4570-bd8e-445bc314247e" name="Prim_in" connectedTo="fffc5ef6-98f4-4e5c-b95d-cf8a44d0076d" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="dc70e32b-f666-46f4-a9c8-cde064c5a9c1" name="Prim_out" connectedTo="d8a93cea-aa5b-495b-ae85-1e31b8360ce5" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:InPort" id="dc266aaf-16e4-48a8-a670-20d36002e0f9" name="Sec_in" connectedTo="ab76fca7-d225-4ba3-b29a-d9965b6df689" carrier="36a55910-fbfb-4c4e-9db2-7000140b90f8"/>
        <port xsi:type="esdl:OutPort" id="3792d0dd-3856-48c7-b55b-22fcd27acdcb" name="Sec_out" connectedTo="84fe1016-63d4-4710-b0a3-e5f067396001" carrier="2225db3f-a223-4144-97f6-553ba911d4d5"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f0986b5a-bd1d-4faa-96f3-fde953a32732" name="Pipe_f098" length="2088.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.149193993673066" lon="4.562261628987906"/>
          <point xsi:type="esdl:Point" lat="52.15909162485124" lon="4.588275102183875"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3ec4b989-4238-4d3c-8621-f1b60ec5e75c" name="In" connectedTo="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
        <port xsi:type="esdl:OutPort" id="fffc5ef6-98f4-4e5c-b95d-cf8a44d0076d" name="Out" connectedTo="4ce16061-1b4e-4570-bd8e-445bc314247e" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="6452b858-ca03-49ea-855b-acf9dfd9a19a" name="Pipe_6452" length="2045.4">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.160618191203284" lon="4.58655804124684"/>
          <point xsi:type="esdl:Point" lat="52.150773550466454" lon="4.561231392425685"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="d8a93cea-aa5b-495b-ae85-1e31b8360ce5" name="In" connectedTo="dc70e32b-f666-46f4-a9c8-cde064c5a9c1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
        <port xsi:type="esdl:OutPort" id="24fa1f65-7f13-48fa-8bc3-49b6f511ba8e" name="Out" connectedTo="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="67fa2195-99d2-4a20-8a62-95527a6d9835" name="Pipe_67fa" length="2668.1">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.15809143229931" lon="4.63412062920253"/>
          <point xsi:type="esdl:Point" lat="52.160091794927524" lon="4.595143345932012"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="9deb1682-5f54-485b-b5c5-bcbeda372b35" name="In" connectedTo="e890f65f-80e7-46fa-8c52-5385324bf686" carrier="36a55910-fbfb-4c4e-9db2-7000140b90f8"/>
        <port xsi:type="esdl:OutPort" id="ab76fca7-d225-4ba3-b29a-d9965b6df689" name="Out" connectedTo="dc266aaf-16e4-48a8-a670-20d36002e0f9" carrier="36a55910-fbfb-4c4e-9db2-7000140b90f8"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="d934d152-f04e-4a1b-b239-e3ed91ec978a" name="Pipe_d934" length="2668.0">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.161670965077235" lon="4.594971639838309"/>
          <point xsi:type="esdl:Point" lat="52.159670673424294" lon="4.633948923108827"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="84fe1016-63d4-4710-b0a3-e5f067396001" name="In" connectedTo="3792d0dd-3856-48c7-b55b-22fcd27acdcb" carrier="2225db3f-a223-4144-97f6-553ba911d4d5"/>
        <port xsi:type="esdl:OutPort" id="52c2357a-d1af-46be-94dc-bd66bebc2503" name="Out" connectedTo="af0904f7-ba1f-4e79-9040-71e08041601b" carrier="2225db3f-a223-4144-97f6-553ba911d4d5"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
