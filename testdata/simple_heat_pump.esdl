<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="1ddb172b-8af1-456f-a802-108fff66f40c" description="" esdlVersion="v2401" name="Untitled EnergySystem" version="4">
  <instance xsi:type="esdl:Instance" id="fb6c06c7-7716-4ba9-ae37-c2640c5e2072" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="ed88aae8-c67d-4946-806b-bd13fe120640">
      <asset xsi:type="esdl:HeatPump" name="HeatPump_80c2" id="HeatPump_80c2">
        <port xsi:type="esdl:InPort" name="PrimIn" id="4612e567-987e-436f-b42a-164e5ac41003" connectedTo="cd75e6a1-d9bc-4c43-88a5-eacc2a3a7c54" carrier="e2b95d83-989a-4a77-971f-435e931a0adf"/>
        <port xsi:type="esdl:OutPort" name="PrimOut" id="2b090a14-ed38-4ddc-9c1e-c8086ed99f1a" connectedTo="61860e7e-9e2c-47f3-bfb9-246a2dde0110" carrier="e2b95d83-989a-4a77-971f-435e931a0adf"/>
        <port xsi:type="esdl:InPort" name="SecIn" id="3051c490-1d26-4bea-8af6-bf8821233b06" connectedTo="0cb011f8-8b44-431f-9584-430e46285142" carrier="448bac5b-224d-46d2-bece-a690bb0c339c"/>
        <port xsi:type="esdl:OutPort" name="SecOut" id="e11b83fa-c124-46f4-b2dd-41649e0075ab" connectedTo="c4da2e55-e843-41e7-8d9a-d9217873ad2a" carrier="448bac5b-224d-46d2-bece-a690bb0c339c"/>
        <geometry xsi:type="esdl:Point" lat="52.051711954437685" lon="4.483494758605958" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericProducer" name="GenericProducer_d46e" id="GenericProducer_d46e" power="100000.0">
        <port xsi:type="esdl:OutPort" name="Out" id="cd75e6a1-d9bc-4c43-88a5-eacc2a3a7c54" connectedTo="4612e567-987e-436f-b42a-164e5ac41003" carrier="e2b95d83-989a-4a77-971f-435e931a0adf"/>
        <port xsi:type="esdl:InPort" name="In" id="61860e7e-9e2c-47f3-bfb9-246a2dde0110" connectedTo="2b090a14-ed38-4ddc-9c1e-c8086ed99f1a" carrier="e2b95d83-989a-4a77-971f-435e931a0adf"/>
        <geometry xsi:type="esdl:Point" lat="52.05161958657236" lon="4.480876922607423" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericConsumer" name="GenericConsumer_2f32" id="GenericConsumer_2f32">
        <port xsi:type="esdl:InPort" name="In" id="c4da2e55-e843-41e7-8d9a-d9217873ad2a" connectedTo="e11b83fa-c124-46f4-b2dd-41649e0075ab" carrier="448bac5b-224d-46d2-bece-a690bb0c339c"/>
        <port xsi:type="esdl:OutPort" name="Out" id="0cb011f8-8b44-431f-9584-430e46285142" connectedTo="3051c490-1d26-4bea-8af6-bf8821233b06" carrier="448bac5b-224d-46d2-bece-a690bb0c339c">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_1700_1950" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="71b11f56-f1d4-4a72-985b-5ec286852d69" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" lat="52.051672368233085" lon="4.485168457031251" CRS="WGS84"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="d4492767-d57b-4524-91e7-ffd92e1d04ec">
    <carriers xsi:type="esdl:Carriers" id="0ab52c8f-87cf-47af-a503-bafeaa055f2c">
      <carrier xsi:type="esdl:HeatCommodity" id="e2b95d83-989a-4a77-971f-435e931a0adf" name="supply" supplyTemperature="40.0" returnTemperature="20.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="448bac5b-224d-46d2-bece-a690bb0c339c" name="hotside" supplyTemperature="80.0" returnTemperature="50.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="7ebbcf07-c57b-457d-929f-0a2b00adb220">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
