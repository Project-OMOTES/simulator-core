<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" version="4" id="fdbbf5ee-6e86-4c82-9926-4b59de482378_with_return_network" description="" esdlVersion="v2207" name="Untitled EnergySystem with return network">
  <instance xsi:type="esdl:Instance" name="Untitled Instance" id="a357cbbe-f277-42b1-8456-cbbadc8ceb2e">
    <area xsi:type="esdl:Area" id="e4002c22-abd5-43f6-81a8-e6b5f960bfa5" name="Untitled Area">
      <asset xsi:type="esdl:HeatingDemand" id="48f3e425-2143-4dcd-9101-c7e22559e82b" name="HeatingDemand_48f3">
        <port xsi:type="esdl:InPort" id="af0904f7-ba1f-4e79-9040-71e08041601b" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="3f2dc09a-0cee-44bd-a337-cea55461a334"/>
        <port xsi:type="esdl:OutPort" connectedTo="422cb921-23d2-4410-9072-aaa5796a0620" id="e890f65f-80e7-46fa-8c52-5385324bf686" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out">
          <profile xsi:type="esdl:InfluxDBProfile" field="demand4_MW" measurement="WarmingUp default profiles" endDate="2019-12-31T22:00:00.000000+0000" port="443" host="profiles.warmingup.info" filters="" startDate="2018-12-31T23:00:00.000000+0000" id="b77e41bc-a5ca-4823-b467-09872f2b6772" database="energy_profiles">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" lon="4.63726043701172" lat="52.158769628869045" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" id="cf3d4b5e-437f-4c1b-a7f9-7fd7e8a269b4" power="5000000.0" name="GenericProducer_cf3d">
        <port xsi:type="esdl:OutPort" connectedTo="a9793a5e-df4f-4795-8079-015dfaf57f82" id="2d818e3d-8a39-4cec-afa0-f6dbbfd50696" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <port xsi:type="esdl:InPort" id="9c258b9d-3149-4720-8931-f4bef1080ec1" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="935fb733-9f76-4a8d-8899-1ad8689a4b12"/>
        <geometry xsi:type="esdl:Point" lon="4.558639526367188" lat="52.148869383489114" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="020ee8b4-9755-4db7-a69e-44e73a6f7385" length="2460.9" name="Pipe1_a" innerDiameter="0.5" related="">
        <port xsi:type="esdl:InPort" id="a9793a5e-df4f-4795-8079-015dfaf57f82" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="2d818e3d-8a39-4cec-afa0-f6dbbfd50696"/>
        <port xsi:type="esdl:OutPort" connectedTo="4f1830d7-8de2-424c-949f-7c37ca554e8f" id="056177cf-f645-4cf4-b785-f2971dbdfda7" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.558639526367188" lat="52.148869383489114"/>
          <point xsi:type="esdl:Point" lon="4.586266279220582" lat="52.16310029390056"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" id="b3810006-a9b1-45a8-8aa2-1ad736883ded" length="3806.07" name="Pipe1_b" innerDiameter="0.5" related="">
        <port xsi:type="esdl:InPort" id="36048944-c211-4dba-8ad5-81e8bcffdcb3" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="13e0d0fc-7196-4ca3-a51f-c649f2ad8b96"/>
        <port xsi:type="esdl:OutPort" connectedTo="af0904f7-ba1f-4e79-9040-71e08041601b" id="3f2dc09a-0cee-44bd-a337-cea55461a334" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.586266279220582" lat="52.16310029390056"/>
          <point xsi:type="esdl:Point" lon="4.594688415527345" lat="52.16740421514521"/>
          <point xsi:type="esdl:Point" lon="4.63726043701172" lat="52.158769628869045"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" id="281f95cd-0eb7-422a-ba9d-104f3e2af4c4" name="Joint_281f">
        <port xsi:type="esdl:InPort" id="4f1830d7-8de2-424c-949f-7c37ca554e8f" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="In" connectedTo="056177cf-f645-4cf4-b785-f2971dbdfda7 8dd9416b-4ce5-4ae8-950b-3d314f3e8112"/>
        <port xsi:type="esdl:OutPort" connectedTo="36048944-c211-4dba-8ad5-81e8bcffdcb3" id="13e0d0fc-7196-4ca3-a51f-c649f2ad8b96" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <geometry xsi:type="esdl:Point" lon="4.586266279220582" lat="52.16310029390056"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="281ac11b-2f47-4b4b-a209-db4fc4850136" length="3792.25" name="Pipe1_ret_a" innerDiameter="0.5" related="">
        <port xsi:type="esdl:InPort" id="422cb921-23d2-4410-9072-aaa5796a0620" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In_ret" connectedTo="e890f65f-80e7-46fa-8c52-5385324bf686"/>
        <port xsi:type="esdl:OutPort" connectedTo="1656016b-e09f-4390-9b73-9311a6770cfe" id="435f8d89-5abc-4af2-a718-cf5cdedab17f" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.636858896813017" lat="52.15885962895904"/>
          <point xsi:type="esdl:Point" lon="4.5942969754153795" lat="52.16749421523521" CRS="WGS84"/>
          <point xsi:type="esdl:Point" lon="4.5860517024993905" lat="52.16324508089198"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" id="3ef3d2a5-2737-4a8f-8c06-1f68a4a5946d" length="2475.23" name="Pipe1_ret_b" innerDiameter="0.5" related="">
        <port xsi:type="esdl:InPort" id="88b9ff74-9d98-419f-a003-ea74bfe863bd" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="4f9c5bbe-dbeb-4566-aaf9-81e04bb2d6ff"/>
        <port xsi:type="esdl:OutPort" connectedTo="9c258b9d-3149-4720-8931-f4bef1080ec1" id="935fb733-9f76-4a8d-8899-1ad8689a4b12" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out_ret"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lon="4.5860517024993905" lat="52.16324508089198"/>
          <point xsi:type="esdl:Point" lon="4.558225705568235" lat="52.14895938357911" CRS="WGS84"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" id="ef185c53-23ba-42c9-8f64-28bcd4518cb5" name="Joint_ef18">
        <port xsi:type="esdl:InPort" id="1656016b-e09f-4390-9b73-9311a6770cfe" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="435f8d89-5abc-4af2-a718-cf5cdedab17f"/>
        <port xsi:type="esdl:OutPort" connectedTo="88b9ff74-9d98-419f-a003-ea74bfe863bd fef07661-feeb-49f2-994a-c9480c67eb90" id="4f9c5bbe-dbeb-4566-aaf9-81e04bb2d6ff" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="Out"/>
        <geometry xsi:type="esdl:Point" lon="4.5860517024993905" lat="52.16324508089198"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" id="702d4624-db23-4b12-b70b-76fd8b72c16a" power="5000000.0" name="GenericProducer_702d">
        <port xsi:type="esdl:OutPort" connectedTo="4f1830d7-8de2-424c-949f-7c37ca554e8f" id="8dd9416b-4ce5-4ae8-950b-3d314f3e8112" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a" name="Out"/>
        <port xsi:type="esdl:InPort" id="fef07661-feeb-49f2-994a-c9480c67eb90" carrier="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret" name="In" connectedTo="4f9c5bbe-dbeb-4566-aaf9-81e04bb2d6ff"/>
        <geometry xsi:type="esdl:Point" lon="4.587339162826539" lat="52.162014376449676"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="c615f17e-c077-48c4-8a78-6ae05f8a908f">
    <carriers xsi:type="esdl:Carriers" id="c27258b1-f4f6-4e09-a77a-ce466dbd82d2">
      <carrier xsi:type="esdl:HeatCommodity" name="HeatSupply" supplyTemperature="80.0" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a"/>
      <carrier xsi:type="esdl:HeatCommodity" name="HeatReturn" returnTemperature="40.0" id="0bd9cb08-2f69-4e97-8ac8-bd87b07e466a_ret"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="f61a1799-bf04-416a-b15e-93097722ada7">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" multiplier="MEGA" unit="WATT" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
