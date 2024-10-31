<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="fdbbf5ee-6e86-4c82-9926-4b59de482378_with_return_network" description="" esdlVersion="v2207" name="Untitled EnergySystem with return network" version="3">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="c615f17e-c077-48c4-8a78-6ae05f8a908f">
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="f61a1799-bf04-416a-b15e-93097722ada7">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" multiplier="MEGA" unit="WATT" description="Power in MW"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" id="12c481c0-f81e-49b6-9767-90457684d24a" multiplier="KILO" unit="WATTHOUR" description="Energy in kWh"/>
    </quantityAndUnits>
    <carriers xsi:type="esdl:Carriers" id="c27258b1-f4f6-4e09-a77a-ce466dbd82d2">
      <carrier xsi:type="esdl:HeatCommodity" supplyTemperature="80.0" name="HeatSupply" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      <carrier xsi:type="esdl:HeatCommodity" returnTemperature="40.0" name="HeatReturn" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="a357cbbe-f277-42b1-8456-cbbadc8ceb2e" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="e4002c22-abd5-43f6-81a8-e6b5f960bfa5">
      <asset xsi:type="esdl:HeatingDemand" id="48f3e425-2143-4dcd-9101-c7e22559e82b" name="HeatingDemand_48f3">
        <port xsi:type="esdl:InPort" connectedTo="3f2dc09a-0cee-44bd-a337-cea55461a334" id="af0904f7-ba1f-4e79-9040-71e08041601b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In"/>
        <port xsi:type="esdl:OutPort" id="e890f65f-80e7-46fa-8c52-5385324bf686" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out" connectedTo="422cb921-23d2-4410-9072-aaa5796a0620">
          <profile xsi:type="esdl:InfluxDBProfile" endDate="2019-12-31T22:00:00.000000+0000" id="b77e41bc-a5ca-4823-b467-09872f2b6772" port="443" host="profiles.warmingup.info" filters="" startDate="2018-12-31T23:00:00.000000+0000" database="energy_profiles" measurement="WarmingUp default profiles" field="demand4_MW">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="4.63726043701172" lat="52.158769628869045"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" power="5000000.0" id="cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4" name="GenericProducer_cf3d">
        <port xsi:type="esdl:InPort" connectedTo="935fb733-9f76-4a8d-8899-1ad8689a4b12" id="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In"/>
		<port xsi:type="esdl:OutPort" id="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out" connectedTo="a9793a5e-df4f-4795-8079-015dfaf57f82"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="4.558639526367188" lat="52.148869383489114"/>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe1_ret" id="Pipe1" length="6267.0" name="Pipe1" innerDiameter="0.1">
        <port xsi:type="esdl:InPort" connectedTo="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" id="a9793a5e-df4f-4795-8079-015dfaf57f82" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In"/>
        <port xsi:type="esdl:OutPort" id="3f2dc09a-0cee-44bd-a337-cea55461a334" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out" connectedTo="af0904f7-ba1f-4e79-9040-71e08041601b"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="4.558639526367188" lat="52.148869383489114"/>
          <point xsi:type="esdl:Point" lon="4.594688415527345" lat="52.16740421514521"/>
          <point xsi:type="esdl:Point" lon="4.63726043701172" lat="52.158769628869045"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" related="Pipe1" id="Pipe1_ret" length="6267.0" name="Pipe1_ret" innerDiameter="0.1">
        <port xsi:type="esdl:InPort" connectedTo="e890f65f-80e7-46fa-8c52-5385324bf686" id="422cb921-23d2-4410-9072-aaa5796a0620" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In_ret"/>
        <port xsi:type="esdl:OutPort" id="935fb733-9f76-4a8d-8899-1ad8689a4b12" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out_ret" connectedTo="9c258b9d-3149-4720-8931-f4bef1080ec1"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lon="4.636858896813017" lat="52.15885962895904"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lon="4.5942969754153795" lat="52.16749421523521"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lon="4.558225705568235" lat="52.14895938357911"/>
        </geometry>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
