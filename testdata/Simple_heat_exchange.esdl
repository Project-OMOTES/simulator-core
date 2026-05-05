<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="1ddb172b-8af1-456f-a802-108fff66f40c" description="" esdlVersion="v2401" name="Untitled EnergySystem" version="4">
  <instance xsi:type="esdl:Instance" id="fb6c06c7-7716-4ba9-ae37-c2640c5e2072" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="ed88aae8-c67d-4946-806b-bd13fe120640">
      <asset xsi:type="esdl:GenericProducer" name="GenericProducer_d46e" id="GenericProducer_d46e">
        <port xsi:type="esdl:OutPort" name="Out" id="cd75e6a1-d9bc-4c43-88a5-eacc2a3a7c54" connectedTo="dbda35fd-e4e0-40d8-ab60-82224151ddd3" carrier="fab8255a-1470-44ee-a5ab-31dcef762d23"/>
        <port xsi:type="esdl:InPort" name="In" id="61860e7e-9e2c-47f3-bfb9-246a2dde0110" connectedTo="08187a2d-996d-4564-8aaf-1b4b888cf4c5" carrier="fab8255a-1470-44ee-a5ab-31dcef762d23"/>
        <geometry xsi:type="esdl:Point" lat="52.05161958657236" lon="4.480876922607423" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:GenericConsumer" name="GenericConsumer_2f32" id="GenericConsumer_2f32">
        <port xsi:type="esdl:InPort" name="In" id="c4da2e55-e843-41e7-8d9a-d9217873ad2a" connectedTo="c7f3a3ef-c1d8-4bf6-a510-e32b980a232a" carrier="43dfcd2d-6140-4e8f-baef-1be3ba137e5f"/>
        <port xsi:type="esdl:OutPort" name="Out" id="0cb011f8-8b44-431f-9584-430e46285142" connectedTo="e4e50963-3429-4c3b-886d-7bf0f8231047" carrier="43dfcd2d-6140-4e8f-baef-1be3ba137e5f">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_1700_1950" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="d95759fe-f7ad-4c00-90ec-5ebf157704f8" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <geometry xsi:type="esdl:Point" lat="52.051672368233085" lon="4.485168457031251" CRS="WGS84"/>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="e395f98d-2e3c-4091-a73d-8a915a418a11" name="HeatExchange_e395">
        <geometry xsi:type="esdl:Point" lat="52.05198245923054" lon="4.48344111442566" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="dbda35fd-e4e0-40d8-ab60-82224151ddd3" name="PrimIn" connectedTo="cd75e6a1-d9bc-4c43-88a5-eacc2a3a7c54" carrier="fab8255a-1470-44ee-a5ab-31dcef762d23"/>
        <port xsi:type="esdl:OutPort" id="08187a2d-996d-4564-8aaf-1b4b888cf4c5" name="PrimOut" connectedTo="61860e7e-9e2c-47f3-bfb9-246a2dde0110" carrier="fab8255a-1470-44ee-a5ab-31dcef762d23"/>
        <port xsi:type="esdl:OutPort" id="c7f3a3ef-c1d8-4bf6-a510-e32b980a232a" name="SecOut" carrier="43dfcd2d-6140-4e8f-baef-1be3ba137e5f" connectedTo="c4da2e55-e843-41e7-8d9a-d9217873ad2a"/>
        <port xsi:type="esdl:InPort" id="e4e50963-3429-4c3b-886d-7bf0f8231047" name="SecIn" carrier="43dfcd2d-6140-4e8f-baef-1be3ba137e5f" connectedTo="0cb011f8-8b44-431f-9584-430e46285142"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="f3d11b93-cab1-403d-b789-e29f5321ac1d">
    <carriers xsi:type="esdl:Carriers" id="002f29e1-2a73-46e0-9bde-9a7229f61875">
      <carrier xsi:type="esdl:HeatCommodity" id="fab8255a-1470-44ee-a5ab-31dcef762d23" name="hotside" supplyTemperature="80.0" returnTemperature="50.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="43dfcd2d-6140-4e8f-baef-1be3ba137e5f" name="coldside" supplyTemperature="60.0" returnTemperature="40.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="7f4efde4-7d28-473b-a2d0-45084a4eabf3">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
