<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="Delft_T_GrowOptimized" description="Asset(s) being optimized: T-transport" id="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" version="23" esdlVersion="v2401">
  <instance xsi:type="esdl:Instance" id="b5d2f9ba-899f-4ed3-a1a6-468083080c29" name="Untitled Instance">
    <area xsi:type="esdl:Area" id="ab5cb07c-1842-4bb1-872f-480a19feabb5" name="Untitled Area">
      <asset xsi:type="esdl:HeatingDemand" id="a11c72f9-a5e8-4e33-9504-7a44a29b9861" name="Buitenhof" power="15000000.0">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.99287787937531" lon="4.336284399032594"/>
        <port xsi:type="esdl:InPort" id="abcec1a4-5a73-460f-bec5-a8a4eaf6e210" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="7e5de7de-014a-42a2-846a-b7f5814043a4">
          <profile xsi:type="esdl:InfluxDBProfile" id="b874a903-cf1d-430d-84d1-0d37f7f732da" multiplier="14.0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" host="https://profiles.warmingup.info" database="energy_profiles" filters="" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_2000_2010">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="2de34c49-31dd-4583-a4f4-3ea83b486fe0" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="29a9bc48-88e3-4ba1-98e6-7c3beda1ccec">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="cea7c239-aa73-4652-9d88-65aa2279f67c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='a11c72f9-a5e8-4e33-9504-7a44a29b9861'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="19b32d34-3133-44a5-baf6-884c0951d38e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='a11c72f9-a5e8-4e33-9504-7a44a29b9861'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="8cf7ab21-57c6-4cbe-bb09-c85dad625d58" name="Voorhof" power="12500000.0">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.9963708675561" lon="4.360003173351289"/>
        <port xsi:type="esdl:InPort" id="f2a3d85d-8ffd-417f-8318-44733cde25ac" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="2ad472b1-9206-4cdb-8868-773a8c17e010">
          <profile xsi:type="esdl:InfluxDBProfile" id="c818b979-ec9d-4308-af6d-da31725fdb87" multiplier="11.0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" host="https://profiles.warmingup.info" database="energy_profiles" filters="" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_1900_2000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="2cdce875-65f6-4ce9-b7dd-c6438b24da2e" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="8312b1b6-b753-4caa-8dfe-9dc834067484">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="345c29b2-715c-4e8b-88aa-d140f6ad592c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='8cf7ab21-57c6-4cbe-bb09-c85dad625d58'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3afc7e46-8ec8-4d8d-8629-6dc545773ba4" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='8cf7ab21-57c6-4cbe-bb09-c85dad625d58'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="5c8d8519-4f57-475f-977d-103eb34a05f4" name="Tanthof Oost" power="10000000.0">
        <geometry xsi:type="esdl:Point" lat="51.988831287615405" lon="4.359710812568665"/>
        <port xsi:type="esdl:InPort" id="e80fdb9d-52ee-4410-8097-0ae5df11f0ef" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="204913ef-b187-4738-8470-e59e7f6a9714">
          <profile xsi:type="esdl:InfluxDBProfile" id="de3378f7-4d12-4d9c-911b-db515083e2a4" multiplier="9.0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" host="https://profiles.warmingup.info" database="energy_profiles" filters="" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_1900_2000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="f0fbe6cf-7439-4a57-9137-c4452e3c7dda" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="e900287d-ee43-41c8-8553-4adf0ba258b7">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1ebacbed-b787-4295-a2a5-3ea6eaad477e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='5c8d8519-4f57-475f-977d-103eb34a05f4'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="476709b6-1adf-47fe-ac14-201fc28e5767" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='5c8d8519-4f57-475f-977d-103eb34a05f4'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="9a85a5a3-d9e6-46a5-ad93-b82bae94a610" name="Tanthof West" power="15000000.0">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.98550455015984" lon="4.34485673904419"/>
        <port xsi:type="esdl:InPort" id="9de82a78-c855-4870-83e8-eb0b1e14ebfb" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="f9a34d85-09b6-4027-bfa0-460e81c71af6">
          <profile xsi:type="esdl:InfluxDBProfile" id="ba1039b5-a536-4eeb-8b67-7c298ce85e47" multiplier="12.0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" host="https://profiles.warmingup.info" database="energy_profiles" filters="" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_1900_2000">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="2554a536-e0fc-47ba-af67-94be7eaeb643" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="e0c29235-31bf-47b7-851f-1c09449aba2b">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="13722893-a361-4288-91af-4112ffce217b" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='9a85a5a3-d9e6-46a5-ad93-b82bae94a610'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6de762d0-bc5b-4b5f-bc8c-0486ab56acd9" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='9a85a5a3-d9e6-46a5-ad93-b82bae94a610'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="79d559de-54f2-40b9-af9a-c62f499db523" name="TUDelft" power="10000000.0">
        <geometry xsi:type="esdl:Point" lat="51.99928395991665" lon="4.372908622026444"/>
        <port xsi:type="esdl:InPort" id="009d4384-b264-4b8c-9b1b-6526e17b065b" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="94f97ff2-e7d4-4282-a64d-2e096030a85f">
          <profile xsi:type="esdl:InfluxDBProfile" id="812bdd68-4c7f-4157-ace4-cabeba622024" multiplier="10.0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" host="https://profiles.warmingup.info" database="energy_profiles" filters="" measurement="Space Heat default profiles" field="SpaceHeat_and_HotWater_PowerProfile_2000_2010">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="6a4e4835-ddee-4652-9cfa-2c8d49821d6f" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="3e844e19-0eff-47e7-af3b-d95e29d0c7f8">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6e95f338-b385-48c0-95f3-28c73668e84e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='79d559de-54f2-40b9-af9a-c62f499db523'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="20722289-0378-4651-9e25-d8eaa3170c09" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='79d559de-54f2-40b9-af9a-c62f499db523'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:GeothermalSource" id="9684c4fc-df93-4ead-8c10-b7b84eef895b" name="GeothermalSource_9684" power="30000000.0">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.9993979035546" lon="4.369286298751832"/>
        <costInformation xsi:type="esdl:CostInformation" id="1a7f44ed-9928-4018-ae89-93fc26006857">
          <investmentCosts xsi:type="esdl:SingleValue" id="deeec39b-f982-47d7-94d8-506a1369832d" value="1360000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="MEGA" perUnit="WATT" description="Cost in EUR/MW" id="c27d23a2-65ea-46d8-af4e-23dbb5aa31a1"/>
          </investmentCosts>
          <variableOperationalCosts xsi:type="esdl:SingleValue" id="cc9a45bd-ad00-46b6-98de-2f49b2bd4ca9" value="2.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="MEGA" perUnit="WATTHOUR" description="Cost in EUR/MWh" id="06dcc290-0b6e-4a29-893a-8fea9b6c621c"/>
          </variableOperationalCosts>
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" id="d972b87e-38aa-41f4-9ab1-f491d318a659" value="91000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="MEGA" perUnit="WATT" description="Cost in EUR/MW" id="ab1c001c-e780-40df-9ae1-cc861bce471e"/>
          </fixedMaintenanceCosts>
        </costInformation>
        <port xsi:type="esdl:OutPort" id="fa77af71-df5c-4ad8-9a1b-c6a68c6d87de" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="2b78d35e-c5f0-4248-9e5b-d2e88bc02985">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="cdb0c92f-39e5-4de3-9939-d3f496d584fd" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='9684c4fc-df93-4ead-8c10-b7b84eef895b'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="20ec1f9f-03ec-405c-9c39-eebc18673983" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='9684c4fc-df93-4ead-8c10-b7b84eef895b'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
        <port xsi:type="esdl:InPort" id="8b9b3b28-f224-4642-8b37-f84fcf540c2e" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="c52483a0-d143-4106-a43b-746311baefe2"/>
      </asset>
      <asset xsi:type="esdl:ResidualHeatSource" id="49c218d4-f760-4ec5-87ac-025edb5b7ade" name="WarmteLinQ" power="30000000.0">
        <geometry xsi:type="esdl:Point" lat="51.99471771893644" lon="4.350060224533082"/>
        <costInformation xsi:type="esdl:CostInformation" id="4e42c17c-099f-4502-97a5-f61a1eb85fff">
          <investmentCosts xsi:type="esdl:SingleValue" id="274b51a2-dd25-4ecd-827e-1ce54ab7ce6a" value="1500.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="KILO" perUnit="WATT" description="Cost in EUR/kW" id="57e7bc0d-d812-4be8-ad02-d6bee030285c"/>
          </investmentCosts>
          <installationCosts xsi:type="esdl:SingleValue" id="27925fa4-a569-47ab-bd3c-96582aced86e" value="100000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" description="Cost in EUR" id="f3841943-2eac-4042-a9e1-0cab7c53634b"/>
          </installationCosts>
          <variableOperationalCosts xsi:type="esdl:SingleValue" id="2b0e678f-609e-4c81-840b-570238b136be" value="8.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="MEGA" perUnit="WATTHOUR" description="Cost in EUR/MWh" id="49989bd5-6da8-4c63-8335-05999f98cb40"/>
          </variableOperationalCosts>
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" id="6d342795-0063-4460-802d-249c4603d8d4" value="29000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="MEGA" perUnit="WATT" description="Cost in EUR/MW" id="a813d44f-0121-4e1d-a4c3-3368f09b57e4"/>
          </fixedMaintenanceCosts>
          <fixedOperationalCosts xsi:type="esdl:SingleValue" id="a2ccb243-24ff-4e8f-b9eb-231061a5dc6c" value="35.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perMultiplier="KILO" perUnit="WATT" description="Cost in EUR/kW" id="cccd7a17-cf1b-42ab-968d-4a08245b7691"/>
          </fixedOperationalCosts>
        </costInformation>
        <port xsi:type="esdl:OutPort" id="577714a4-c560-4b64-a70e-09bf12a65b1c" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="479a2393-d053-4a67-bc54-ea7ee755df37">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="33f25358-949d-46bb-a11b-c34ee4cc549e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='49c218d4-f760-4ec5-87ac-025edb5b7ade'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="57e247f2-ffef-4bed-bcae-ec43ddc642d7" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='49c218d4-f760-4ec5-87ac-025edb5b7ade'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
        <port xsi:type="esdl:InPort" id="3bef437b-1f74-4920-be2c-14d60e9d5e79" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="6631bbc0-4696-4426-88af-82a79f8ecbe8"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="0602f235-45dc-47f7-9e7b-7ca06a04cbef" name="Joint_0602">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.99483002267327" lon="4.350956082344056"/>
        <port xsi:type="esdl:InPort" id="52ab4605-e440-4362-8b6a-1da389276935" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="f67a61ad-623d-4280-b28a-936e51978630"/>
        <port xsi:type="esdl:OutPort" id="149aacff-a165-4d36-af77-fbb1c5c93ae4" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="1dcbfe8e-c388-46f4-b247-ad34ecbf7c42 bbf4b6d0-6840-48b2-825c-dd606c2be162"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe1" name="Pipe1" innerDiameter="0.3938" outerDiameter="0.56" length="63.9" diameter="DN400" related="Pipe1_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="51.994716067408795" lon="4.350041449069978"/>
          <point xsi:type="esdl:Point" lat="51.99483002267327" lon="4.350956082344056"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="e133f20c-69af-493a-8284-37f8c6a3de0d">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="2840.6">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0063">
            <matter xsi:type="esdl:Material" id="74d84321-1767-4cec-b6e7-b90c06020400" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0711">
            <matter xsi:type="esdl:Material" id="95012cd9-7648-4df5-8c83-74dc73bc16ba" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0057">
            <matter xsi:type="esdl:Material" id="1392ee3f-34f6-4c8e-ab0e-635b9d7ec9be" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="479a2393-d053-4a67-bc54-ea7ee755df37" name="In" connectedTo="577714a4-c560-4b64-a70e-09bf12a65b1c" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="f67a61ad-623d-4280-b28a-936e51978630" name="Out" connectedTo="52ab4605-e440-4362-8b6a-1da389276935" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="39cbc51f-3276-4929-92ac-146ec702081e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="68185ccc-d1f8-4ebe-acf4-3557283c74bb" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1feb6853-9c0a-42dc-81e2-8900577f7bd8" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c3b2f45a-566c-4558-a069-536362e3319a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe2" name="Pipe2" innerDiameter="0.263" outerDiameter="0.4" length="1358.7" diameter="DN250" related="Pipe2_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="51.99483002267327" lon="4.350956082344056"/>
          <point xsi:type="esdl:Point" lat="51.99644188056501" lon="4.350264072418214"/>
          <point xsi:type="esdl:Point" lat="51.9957020185738" lon="4.345843791961671"/>
          <point xsi:type="esdl:Point" lat="51.99586716739971" lon="4.3448781967163095"/>
          <point xsi:type="esdl:Point" lat="51.994327956723374" lon="4.344298839569093"/>
          <point xsi:type="esdl:Point" lat="51.99383249138507" lon="4.340769052505494"/>
          <point xsi:type="esdl:Point" lat="51.993218106751065" lon="4.337282180786134"/>
          <point xsi:type="esdl:Point" lat="51.99313883070034" lon="4.3360376358032235"/>
          <point xsi:type="esdl:Point" lat="51.99287787937531" lon="4.336284399032594"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="0d01156b-596d-4998-a6c6-e58416fc9213">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="1dcbfe8e-c388-46f4-b247-ad34ecbf7c42" name="In" connectedTo="149aacff-a165-4d36-af77-fbb1c5c93ae4" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="7e5de7de-014a-42a2-846a-b7f5814043a4" name="Out" connectedTo="abcec1a4-5a73-460f-bec5-a8a4eaf6e210" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="2b146261-4086-4ff1-af7d-ce2ccd6c6e0d" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3611f502-6030-4ce9-ad7f-db2109c3a736" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="96fc4578-3675-4760-b31d-c299ae5d69ab" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6ffbf005-75de-4b15-b697-3d00960b421a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe3" name="Pipe3" innerDiameter="0.263" outerDiameter="0.4" length="393.93" diameter="DN250" related="Pipe3_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.99483002267327" lon="4.350956082344056"/>
          <point xsi:type="esdl:Point" lat="51.99418096924502" lon="4.351299405097962"/>
          <point xsi:type="esdl:Point" lat="51.99410169489909" lon="4.351382553577424"/>
          <point xsi:type="esdl:Point" lat="51.99395800978932" lon="4.351578354835511"/>
          <point xsi:type="esdl:Point" lat="51.994435306824016" lon="4.354295432567597"/>
          <point xsi:type="esdl:Point" lat="51.99453935359899" lon="4.3554139137268075"/>
          <point xsi:type="esdl:Point" lat="51.99460541491795" lon="4.355617761611939"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="526493c7-72b6-40fc-a63c-acb830ceb630">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="bbf4b6d0-6840-48b2-825c-dd606c2be162" name="In" connectedTo="149aacff-a165-4d36-af77-fbb1c5c93ae4" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="0dd107f2-c1fd-4288-baeb-2f3c8271d781" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="6c855627-c430-48d7-a6c5-fd9743525713">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ee6ea9a0-f5f9-43af-a826-cd1293598c91" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="06681c9e-2600-4648-9bbb-d13781e7e26f" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3d4e6ce8-d31d-463e-aae4-7d7195e15a7c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3aa44665-481d-4242-ad2a-1401365952a0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe4" name="Pipe4" innerDiameter="0.263" outerDiameter="0.4" length="484.9" diameter="DN250" related="Pipe4_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.99460541491795" lon="4.355617761611939"/>
          <point xsi:type="esdl:Point" lat="51.99520656844105" lon="4.358192682266236"/>
          <point xsi:type="esdl:Point" lat="51.996230492672275" lon="4.357559680938722"/>
          <point xsi:type="esdl:Point" lat="51.99638242782106" lon="4.3584609031677255"/>
          <point xsi:type="esdl:Point" lat="51.99625031032962" lon="4.359673261642457"/>
          <point xsi:type="esdl:Point" lat="51.9963708675561" lon="4.360003173351289"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="526493c7-72b6-40fc-a63c-acb830ceb630">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="964df08b-9382-4fdf-8702-20f76758b8df" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="49117fc6-1ec2-4a7c-b432-78fabbe33029"/>
        <port xsi:type="esdl:OutPort" id="2ad472b1-9206-4cdb-8868-773a8c17e010" name="Out" connectedTo="f2a3d85d-8ffd-417f-8318-44733cde25ac" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ea711106-d07c-4d20-b610-7f90ecba3792" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="7da2dee9-e4de-4104-ad96-86b1b49141a2" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="faef579e-35f2-4f53-b05d-f211e5118c9d" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ab0152ea-8d22-408d-b400-12f9550a946e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="6a29891f-6712-4675-af74-72a2da1ae999" name="Joint_6a29">
        <geometry xsi:type="esdl:Point" lat="51.99460541491795" lon="4.355617761611939"/>
        <port xsi:type="esdl:InPort" id="6c855627-c430-48d7-a6c5-fd9743525713" name="In" connectedTo="0dd107f2-c1fd-4288-baeb-2f3c8271d781" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="49117fc6-1ec2-4a7c-b432-78fabbe33029" name="Out" connectedTo="964df08b-9382-4fdf-8702-20f76758b8df 52d841d7-c0d3-45bf-adb9-e26d81b0f49d" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe5" name="Pipe5" innerDiameter="0.263" outerDiameter="0.4" length="223.2" diameter="DN250" related="Pipe5_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.99460541491795" lon="4.355617761611939"/>
          <point xsi:type="esdl:Point" lat="51.99272923553559" lon="4.356776475906373"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="439a7891-9620-4d6f-9634-9a68cbdf226c">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="52d841d7-c0d3-45bf-adb9-e26d81b0f49d" name="In" connectedTo="49117fc6-1ec2-4a7c-b432-78fabbe33029" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="b53856b1-ed70-4798-b319-6d19285faf0b" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="b70e4357-f83c-411c-9398-5788de26844b">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f891c3ce-cf41-4d5c-a971-37c98afcbbc2" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c37418a7-6b2c-4996-a6f1-faea6b92f704" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="21a96efa-d94c-4d25-b75a-4d1e9462334a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4cca3587-a6ef-4ff4-8220-f84f0124de47" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="dff991c2-f10a-4f0b-a96c-eac64ffc9fa5" name="Joint_dff9">
        <geometry xsi:type="esdl:Point" lat="51.99272923553559" lon="4.356776475906373"/>
        <port xsi:type="esdl:InPort" id="b70e4357-f83c-411c-9398-5788de26844b" name="In" connectedTo="b53856b1-ed70-4798-b319-6d19285faf0b" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="722edfd1-7ad4-473c-aba3-134b5b59a729" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="a3e6d19a-77fb-4de9-82c4-8f699fb96e65 edd0ab42-3adc-4d41-9c7e-f40f9ae1c079"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe6" name="Pipe6" innerDiameter="0.263" outerDiameter="0.4" length="1690.3" diameter="DN250" related="Pipe6_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="51.99272923553559" lon="4.356776475906373"/>
          <point xsi:type="esdl:Point" lat="51.992372488306984" lon="4.355274438858033"/>
          <point xsi:type="esdl:Point" lat="51.99189682091413" lon="4.352710247039796"/>
          <point xsi:type="esdl:Point" lat="51.992412127028295" lon="4.352324008941651"/>
          <point xsi:type="esdl:Point" lat="51.99191003396547" lon="4.349373579025269"/>
          <point xsi:type="esdl:Point" lat="51.99094547096928" lon="4.349910020828248"/>
          <point xsi:type="esdl:Point" lat="51.990251765558796" lon="4.346058368682862"/>
          <point xsi:type="esdl:Point" lat="51.99004695524001" lon="4.34612274169922"/>
          <point xsi:type="esdl:Point" lat="51.989921425871884" lon="4.345049858093263"/>
          <point xsi:type="esdl:Point" lat="51.99002052803386" lon="4.3442773818969735"/>
          <point xsi:type="esdl:Point" lat="51.98775433709859" lon="4.344288110733033"/>
          <point xsi:type="esdl:Point" lat="51.987106832910484" lon="4.344545602798463"/>
          <point xsi:type="esdl:Point" lat="51.98591751511481" lon="4.344073534011842"/>
          <point xsi:type="esdl:Point" lat="51.985435171673814" lon="4.343891143798829"/>
          <point xsi:type="esdl:Point" lat="51.98550455015984" lon="4.34485673904419"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="f5f69d21-ea71-4559-b777-4bd90df73f82">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="edd0ab42-3adc-4d41-9c7e-f40f9ae1c079" name="In" connectedTo="722edfd1-7ad4-473c-aba3-134b5b59a729" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="f9a34d85-09b6-4027-bfa0-460e81c71af6" name="Out" connectedTo="9de82a78-c855-4870-83e8-eb0b1e14ebfb" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="762310e4-66e8-4111-aed8-68fb4574909c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="08737de4-8c35-4f50-be23-11fb1352840d" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="cf60f0bd-a9e4-4af2-a703-8a3c246cc6b4" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8ff36e90-f8ff-43f3-a290-c92bbb4b4c25" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe7" name="Pipe7" innerDiameter="0.263" outerDiameter="0.4" length="403.93" diameter="DN250" related="Pipe7_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.99272923553559" lon="4.356776475906373"/>
          <point xsi:type="esdl:Point" lat="51.992412127028295" lon="4.356948137283326"/>
          <point xsi:type="esdl:Point" lat="51.99057549608771" lon="4.358053207397462"/>
          <point xsi:type="esdl:Point" lat="51.989333415199866" lon="4.358868598937989"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="439a7891-9620-4d6f-9634-9a68cbdf226c">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="a3e6d19a-77fb-4de9-82c4-8f699fb96e65" name="In" connectedTo="722edfd1-7ad4-473c-aba3-134b5b59a729" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="3f4cfc75-908d-4cbd-a268-3e455ccbfc2a" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="c37bb2ed-d06d-454b-863e-a899b063f965">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e185fdad-e840-4ec5-b6c7-31de4e257250" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="37d9b58e-23de-4418-8bc8-f2cc5d2ddedc" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c11ce7b0-e2a6-4da2-84ba-a37cb67d96b5" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d91b398b-3a93-4745-b10d-6a0667632064" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe8" name="Pipe8" innerDiameter="0.2101" outerDiameter="0.315" length="104.18" diameter="DN200" related="Pipe8_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.989333415199866" lon="4.358868598937989"/>
          <point xsi:type="esdl:Point" lat="51.988732182821614" lon="4.359276294708253"/>
          <point xsi:type="esdl:Point" lat="51.988831287615405" lon="4.359710812568665"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="439a7891-9620-4d6f-9634-9a68cbdf226c">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1355.3">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0045">
            <matter xsi:type="esdl:Material" id="930aa5cf-b76e-4049-afa7-ea79445faf55" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.04385">
            <matter xsi:type="esdl:Material" id="f6bd7242-b1a3-4b24-9edd-ad58a830444b" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="81df81a9-ac8b-4c9d-8d71-dd2bbee92fa3" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="c525a3e2-b021-484d-9e45-062e371b4d03" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="7c3ee187-3368-4672-bf37-f890454abf1b"/>
        <port xsi:type="esdl:OutPort" id="204913ef-b187-4738-8470-e59e7f6a9714" name="Out" connectedTo="e80fdb9d-52ee-4410-8097-0ae5df11f0ef" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="bbf788fb-7be4-4256-ba01-d0e7bb4b80e5" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="91ef28b2-46e6-433c-b739-925404c2a189" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d7903077-c409-4ced-a761-f85446fadfab" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4d38750d-992e-480b-84f5-7f191940a9c4" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="35aaffb9-9664-49ca-ac6e-230e4c5a2ef7" name="Joint_35aa">
        <geometry xsi:type="esdl:Point" lat="51.989333415199866" lon="4.358868598937989"/>
        <port xsi:type="esdl:InPort" id="c37bb2ed-d06d-454b-863e-a899b063f965" name="In" connectedTo="3f4cfc75-908d-4cbd-a268-3e455ccbfc2a fd13043b-7aa5-42ee-9804-fde0d8380177" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="7c3ee187-3368-4672-bf37-f890454abf1b" name="Out" connectedTo="c525a3e2-b021-484d-9e45-062e371b4d03" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe9" name="Pipe9" innerDiameter="0.3444" outerDiameter="0.5" length="53.2" diameter="DN350" related="Pipe9_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.9993979035546" lon="4.369286298751832"/>
          <point xsi:type="esdl:Point" lat="51.99907826201701" lon="4.368723873049022"/>
          <point xsi:type="esdl:Point" lat="51.999074804467746" lon="4.368713647127152"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="2b31fbcd-64ee-421c-b50e-ef95d8369821">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="2360.9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="d2298eee-877b-45e1-8b67-cc63fc2f6c69" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0666">
            <matter xsi:type="esdl:Material" id="cd3d98cc-58f2-4683-8523-7e4183c7e685" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="3979c7f7-6acf-4a32-81bb-8ed118357c6b" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="2b78d35e-c5f0-4248-9e5b-d2e88bc02985" name="In" connectedTo="fa77af71-df5c-4ad8-9a1b-c6a68c6d87de" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="5229a3e7-7b3d-483e-8860-b81d703356dc" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="2ff91621-5f74-4bf1-baf2-e843907ee452">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="98b794ca-6ee8-4431-9939-6b2bd90ce670" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d6be7185-c825-44f7-84fe-f5fe9e225465" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="cb0a7718-ff79-462b-a025-3c4f7521cb7d" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4407c384-7c3e-4a2f-b56e-f47a8b4f63f9" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe11" name="Pipe11" innerDiameter="0.3444" outerDiameter="0.5" length="102.7" diameter="DN350" related="Pipe11_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.99907010839291" lon="4.368712976574899"/>
          <point xsi:type="esdl:Point" lat="51.998195700993726" lon="4.369195103645326"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="2b31fbcd-64ee-421c-b50e-ef95d8369821">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="2360.9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="d2298eee-877b-45e1-8b67-cc63fc2f6c69" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0666">
            <matter xsi:type="esdl:Material" id="cd3d98cc-58f2-4683-8523-7e4183c7e685" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="3979c7f7-6acf-4a32-81bb-8ed118357c6b" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="1343b0ed-fafc-4677-9e5f-e38b13a73017" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="0def0a64-c010-4ef8-9834-b152e7e85884"/>
        <port xsi:type="esdl:OutPort" id="978d0d30-b56b-4b2b-85d1-187585acc6c0" name="Out" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="8cc49167-e8ac-4063-ace2-7715b7e4c7e9">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6dc59a03-5b1d-4be5-9d70-5a6d868db467" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8e90a983-8622-48bf-b9a1-c4c942d78c3f" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1f0c23bd-7224-44a7-b880-14a5990ae7e5" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ae1b87e4-58ee-40db-b504-1c945acebca2" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe12" name="Pipe12" innerDiameter="0.263" outerDiameter="0.4" length="1695.06" diameter="DN250" related="Pipe12_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="51.998195700993726" lon="4.369195103645326"/>
          <point xsi:type="esdl:Point" lat="51.99689107652307" lon="4.369930028915406"/>
          <point xsi:type="esdl:Point" lat="51.9963626102222" lon="4.370251893997193"/>
          <point xsi:type="esdl:Point" lat="51.99252443654816" lon="4.372708797454835"/>
          <point xsi:type="esdl:Point" lat="51.991962886131965" lon="4.369876384735108"/>
          <point xsi:type="esdl:Point" lat="51.991665591884065" lon="4.36783790588379"/>
          <point xsi:type="esdl:Point" lat="51.99131544279403" lon="4.3664753437042245"/>
          <point xsi:type="esdl:Point" lat="51.99050942882292" lon="4.364136457443238"/>
          <point xsi:type="esdl:Point" lat="51.9895514425295" lon="4.359169006347657"/>
          <point xsi:type="esdl:Point" lat="51.989333415199866" lon="4.358868598937989"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="2b31fbcd-64ee-421c-b50e-ef95d8369821">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1630.7">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="8d148f66-5ee2-4b70-9d2c-e6038be94ada" name="In" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" connectedTo="c264080b-5f9b-4bad-bd85-9f963dae742b"/>
        <port xsi:type="esdl:OutPort" id="fd13043b-7aa5-42ee-9804-fde0d8380177" name="Out" connectedTo="c37bb2ed-d06d-454b-863e-a899b063f965" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d63e8c13-4a08-48de-a696-06fba6a37bcc" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="2860ecef-99e0-4b59-870d-92f61e8c3301" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b965c08e-e793-4bc3-a863-32a0ed4fbdf3" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e9920627-908f-4e53-b7c4-e944e7324d31" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="b4633ecb-cda5-4343-9d51-af350a9c331b" name="Joint_b463">
        <geometry xsi:type="esdl:Point" lat="51.998195700993726" lon="4.369195103645326"/>
        <port xsi:type="esdl:InPort" id="8cc49167-e8ac-4063-ace2-7715b7e4c7e9" name="In" connectedTo="978d0d30-b56b-4b2b-85d1-187585acc6c0" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="c264080b-5f9b-4bad-bd85-9f963dae742b" name="Out" connectedTo="8d148f66-5ee2-4b70-9d2c-e6038be94ada dae970c0-5471-4ff2-8da5-802856320750" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe13" name="Pipe13" innerDiameter="0.2101" outerDiameter="0.315" length="285.9" diameter="DN200" related="Pipe13_ret">
        <dataSource xsi:type="esdl:DataSource" name="Logstor Product Catalogue Version 2020.03" attribution="https://www.logstor.com/media/6506/product-catalogue-uk-202003.pdf"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="51.998195700993726" lon="4.369195103645326"/>
          <point xsi:type="esdl:Point" lat="51.99913038325009" lon="4.372783899307252"/>
          <point xsi:type="esdl:Point" lat="51.99928395991665" lon="4.372908622026444"/>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="5ab69aac-efed-4ade-8dd3-96720cd2a96f">
          <investmentCosts xsi:type="esdl:SingleValue" name="Combined investment and installation costs" id="1b0e8f56-b993-4135-ab6b-7e96da963344" value="1355.3">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO" perUnit="METRE" description="Costs in EUR/m" id="6be7a1d2-545f-4d47-9138-818cc03c63f1"/>
          </investmentCosts>
        </costInformation>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0045">
            <matter xsi:type="esdl:Material" id="930aa5cf-b76e-4049-afa7-ea79445faf55" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.04385">
            <matter xsi:type="esdl:Material" id="f6bd7242-b1a3-4b24-9edd-ad58a830444b" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="81df81a9-ac8b-4c9d-8d71-dd2bbee92fa3" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
        <port xsi:type="esdl:InPort" id="dae970c0-5471-4ff2-8da5-802856320750" name="In" connectedTo="c264080b-5f9b-4bad-bd85-9f963dae742b" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="94f97ff2-e7d4-4282-a64d-2e096030a85f" name="Out" connectedTo="009d4384-b264-4b8c-9b1b-6526e17b065b" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="50012b31-ed62-48a1-84a1-d8cd80b5c22d" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="476536b5-ea98-4a79-9a43-18de679f8c13" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9805c1d2-2c11-407a-8d38-8be75c2c5a60" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="de7de18b-4d50-490c-a0b1-c1fa07a6af9e" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" field="PostProc.Pressure"/>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="c2e017f0-3abb-40c5-8407-cfbe0ec2c947" name="Joint_c2e0">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.99907274025906" lon="4.368709498085082"/>
        <port xsi:type="esdl:InPort" id="2ff91621-5f74-4bf1-baf2-e843907ee452" name="In" connectedTo="5229a3e7-7b3d-483e-8860-b81d703356dc" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
        <port xsi:type="esdl:OutPort" id="0def0a64-c010-4ef8-9834-b152e7e85884" name="Out" connectedTo="1343b0ed-fafc-4677-9e5f-e38b13a73017" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="bcf07b56-c3ee-42a6-9c42-9845f5bf0d33" name="Joint_0602_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.99492002276327" lon="4.350150066040208"/>
        <port xsi:type="esdl:OutPort" id="e74f13f2-c63e-4717-b237-6499c9488eac" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="0091722b-9afb-4475-b559-380e270cca80"/>
        <port xsi:type="esdl:InPort" id="8411ac81-9c78-4d11-8a69-f95c26f71033" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="d7de09b1-6d03-4d7e-87da-1896af9f05ad 51c50f83-1e9f-4db1-b8d4-7db3d01807e6"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="8b6a23bf-e9c8-48e2-9984-6184ea7eaae4" name="Joint_6a29_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.994695415007946" lon="4.3548106114555685"/>
        <port xsi:type="esdl:InPort" id="e6a7a2e5-acb6-4084-b3ec-f0df5bbab853" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="f2d10d3d-0064-4cb8-bd02-ae507bd5f3df 8a29b3c1-cd96-43e0-b918-22551a2d139d"/>
        <port xsi:type="esdl:OutPort" id="588fd953-2a7d-4549-a89c-80b27e24ab2c" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="d8daa8a8-f473-4a23-8732-a8ff6379cd67"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="9569e5ad-87e3-4393-82b2-0dd82f2ac12c" name="Joint_dff9_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.99281923562559" lon="4.355959726802834"/>
        <port xsi:type="esdl:InPort" id="c97aaf10-6edc-4518-9339-d8ca7cc0d795" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="95aaf0a1-5641-48ad-bc84-23e0e189c8bf 53bf9474-b529-4831-bee0-5bdfa44c8635"/>
        <port xsi:type="esdl:OutPort" id="525a8a13-4931-4d8d-bb60-adb555b02401" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="ab88819c-46a1-423b-8db8-6b3019fe592f"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="1ff5e86e-3d8f-4ca5-96d6-039ee51938d8" name="Joint_35aa_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.98942341528986" lon="4.358033875102766"/>
        <port xsi:type="esdl:InPort" id="f786a7bf-f26b-4a30-9e21-3fec05412c64" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="309cd564-3412-4022-a6d0-ae705f25be6f"/>
        <port xsi:type="esdl:OutPort" id="ba357584-609f-4cf2-aedd-0fac5c8ceade" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="1a0c09e4-00da-40fd-a96f-6def4dc207d9 15cec74a-ff3d-4349-99c1-b63e54984020"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="6c7199eb-9b16-462c-b713-d06d9d9af554" name="Joint_b463_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.998285701083724" lon="4.368405699422867"/>
        <port xsi:type="esdl:InPort" id="9499403a-8dcf-4c77-944d-a56829b8ff7e" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="a2336831-a837-4c16-8b13-5ccaf7ad4b28 b60cdb49-a624-4274-8daf-c769bc46d984"/>
        <port xsi:type="esdl:OutPort" id="b57116bc-1f78-402c-84c0-fc6e5846cf8a" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="03f16a92-b24d-4e11-b730-83b703517cad"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="6f4114b7-8755-464f-9de3-e215e1e08ae6" name="Joint_c2e0_ret">
        <geometry xsi:type="esdl:Point" CRS="WGS84" lat="51.99916274034906" lon="4.367924309381006"/>
        <port xsi:type="esdl:InPort" id="81a1bb4a-1701-4491-86d4-2c2f0b858aa2" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="1207cf4b-308c-4466-b1c8-9e997e988fff"/>
        <port xsi:type="esdl:OutPort" id="c0bdb043-c1ec-455f-92f2-eabbbcb8580a" name="ret_port" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" connectedTo="3c52ca3a-e59e-4fff-a451-fc110907d9aa"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe1_ret" name="Pipe1_ret" innerDiameter="0.3938" outerDiameter="0.56" length="63.9" diameter="DN400" related="Pipe1">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99492002276327" lon="4.350150066040208"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99480606749879" lon="4.349234857906909"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="0091722b-9afb-4475-b559-380e270cca80" name="In_ret" connectedTo="e74f13f2-c63e-4717-b237-6499c9488eac" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="6631bbc0-4696-4426-88af-82a79f8ecbe8" name="Out_ret" connectedTo="3bef437b-1f74-4920-be2c-14d60e9d5e79" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f44c5d3f-042e-49f9-a439-dec70e20cab0" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c555049b-a514-40dc-9de2-9db1b24b5ab3" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="76ce9705-d5da-44d5-9c81-12520aba84bc" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6b973fcf-11da-46cf-a898-bc02ec7fd360" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe1_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0063">
            <matter xsi:type="esdl:Material" id="74d84321-1767-4cec-b6e7-b90c06020400" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0711">
            <matter xsi:type="esdl:Material" id="95012cd9-7648-4df5-8c83-74dc73bc16ba" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0057">
            <matter xsi:type="esdl:Material" id="1392ee3f-34f6-4c8e-ab0e-635b9d7ec9be" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe2_ret" name="Pipe2_ret" innerDiameter="0.263" outerDiameter="0.4" length="1358.7" diameter="DN250" related="Pipe2">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.992967879465304" lon="4.335468418848538"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.993228830790336" lon="4.335223001954349"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99330810684106" lon="4.336467955058524"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99392249147507" lon="4.339957975709468"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99441795681337" lon="4.343490284295128"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.995957167489706" lon="4.344077374497806"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.9957920186638" lon="4.3450421472109175"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.996531880655006" lon="4.349466099308366"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99492002276327" lon="4.350150066040208"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="29a9bc48-88e3-4ba1-98e6-7c3beda1ccec" name="In_ret" connectedTo="2de34c49-31dd-4583-a4f4-3ea83b486fe0" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="d7de09b1-6d03-4d7e-87da-1896af9f05ad" name="Out_ret" connectedTo="8411ac81-9c78-4d11-8a69-f95c26f71033" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c97a5a58-1235-437d-9581-9f2815b9c011" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="33bdad50-d4ea-48dc-b1bf-9519945c166a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1a5c8762-725c-48db-ac92-e3ac6e59670c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="74ab3705-2171-40c0-8cfb-69c56915155f" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe2_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe3_ret" name="Pipe3_ret" innerDiameter="0.263" outerDiameter="0.4" length="393.93" diameter="DN250" related="Pipe3">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.994695415007946" lon="4.3548106114555685"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.994629353688985" lon="4.3546064294682"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.994525306914014" lon="4.353487421528576"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.994048009879315" lon="4.350767918332793"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99419169498909" lon="4.350572848784311"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99427096933502" lon="4.35049010343325"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99492002276327" lon="4.350150066040208"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="d8daa8a8-f473-4a23-8732-a8ff6379cd67" name="In_ret" connectedTo="588fd953-2a7d-4549-a89c-80b27e24ab2c" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="51c50f83-1e9f-4db1-b8d4-7db3d01807e6" name="Out_ret" connectedTo="8411ac81-9c78-4d11-8a69-f95c26f71033" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9e3d3dcf-0814-41e6-83cf-460d4ae6c963" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="fe666cae-fc89-4b7d-b9d1-b488a1bc10af" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ef8713ef-0884-4228-829f-d1b8cc0d0824" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="82ae93db-1415-4857-90ac-da44066429c5" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe3_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe4_ret" name="Pipe4_ret" innerDiameter="0.263" outerDiameter="0.4" length="484.9" diameter="DN250" related="Pipe4">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.9964608676461" lon="4.359204849310848"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99634031041962" lon="4.358874341118289"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99647242791106" lon="4.357662636276866"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99632049276227" lon="4.356760662275853"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.995296568531046" lon="4.357388559599185"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.994695415007946" lon="4.3548106114555685"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="8312b1b6-b753-4caa-8dfe-9dc834067484" name="In_ret" connectedTo="2cdce875-65f6-4ce9-b7dd-c6438b24da2e" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="f2d10d3d-0064-4cb8-bd02-ae507bd5f3df" name="Out_ret" connectedTo="e6a7a2e5-acb6-4084-b3ec-f0df5bbab853" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="947fbdbd-7440-45d6-9e40-30ab14f58d56" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="772da937-f1c2-4660-a0a6-dba07410b4ef" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f04d6d39-0141-4ac7-b286-407931db01df" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="509d301e-10bb-46c9-8074-809d0a2fa7fa" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe4_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe5_ret" name="Pipe5_ret" innerDiameter="0.263" outerDiameter="0.4" length="223.2" diameter="DN250" related="Pipe5">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99281923562559" lon="4.355959726802834"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.994695415007946" lon="4.3548106114555685"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="ab88819c-46a1-423b-8db8-6b3019fe592f" name="In_ret" connectedTo="525a8a13-4931-4d8d-bb60-adb555b02401" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="8a29b3c1-cd96-43e0-b918-22551a2d139d" name="Out_ret" connectedTo="e6a7a2e5-acb6-4084-b3ec-f0df5bbab853" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="96f08000-00b2-4fa3-8183-928469e9456b" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="fe3c91cc-452c-4043-911b-c883bd560a8c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="7fccc537-d417-42a2-b959-c2b97ae2a936" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="94e39011-c8f0-4afa-be44-b3b0294c3d86" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe5_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe6_ret" name="Pipe6_ret" innerDiameter="0.263" outerDiameter="0.4" length="1690.3" diameter="DN250" related="Pipe6">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.985594550249836" lon="4.3440007630795785"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98552517176381" lon="4.343034772645288"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.986007515204804" lon="4.343219902738562"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98719683300048" lon="4.343698652108816"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98784433718859" lon="4.343444752901676"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99011052812386" lon="4.343446359422575"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99001142596188" lon="4.34421830382353"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99013695533001" lon="4.345291860920478"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99034176564879" lon="4.345228584386799"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99103547105928" lon="4.349083928725807"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.992000034055465" lon="4.348552565812081"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99250212711829" lon="4.351505614554315"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.991986821004126" lon="4.35188916468059"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99246248839698" lon="4.354455838337416"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99281923562559" lon="4.355959726802834"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e0c29235-31bf-47b7-851f-1c09449aba2b" name="In_ret" connectedTo="2554a536-e0fc-47ba-af67-94be7eaeb643" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="95aaf0a1-5641-48ad-bc84-23e0e189c8bf" name="Out_ret" connectedTo="c97aaf10-6edc-4518-9339-d8ca7cc0d795" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9f133667-47fd-42e2-a77b-e34a57b75343" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="586f02a3-b17e-4edb-9651-3facaed7e4c6" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c92dd035-0d88-4404-8e9b-ebfe429b040c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="efb99d21-657d-409a-b8b3-6e233ee4c5fe" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe6_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe7_ret" name="Pipe7_ret" innerDiameter="0.263" outerDiameter="0.4" length="403.93" diameter="DN250" related="Pipe7">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98942341528986" lon="4.358033875102766"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.990665496177705" lon="4.357225150280455"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99250212711829" lon="4.35612974289599"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99281923562559" lon="4.355959726802834"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="1a0c09e4-00da-40fd-a96f-6def4dc207d9" name="In_ret" connectedTo="ba357584-609f-4cf2-aedd-0fac5c8ceade" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="53bf9474-b529-4831-bee0-5bdfa44c8635" name="Out_ret" connectedTo="c97aaf10-6edc-4518-9339-d8ca7cc0d795" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="18cfc099-4b50-4f5b-a2ce-ddaa1700d262" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="017ab38e-e313-4953-8ff0-491899d47c03" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="2aaeb3c3-fc46-472d-9670-34feb506751c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ed48d877-4629-440c-9589-b436115f7b9a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe7_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe8_ret" name="Pipe8_ret" innerDiameter="0.2101" outerDiameter="0.315" length="104.18" diameter="DN200" related="Pipe8">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.9889212877054" lon="4.3588733626863565"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98882218291161" lon="4.358438304656425"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98942341528986" lon="4.358033875102766"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e900287d-ee43-41c8-8553-4adf0ba258b7" name="In_ret" connectedTo="f0fbe6cf-7439-4a57-9137-c4452e3c7dda" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="309cd564-3412-4022-a6d0-ae705f25be6f" name="Out_ret" connectedTo="f786a7bf-f26b-4a30-9e21-3fec05412c64" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e154f491-eab6-4986-b2d6-f36f271ddde5" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c4e9779b-1291-467d-8262-1f8e33f8a1eb" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="60d06a13-fe0b-4c15-9591-3395466453f4" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c79b96b0-9da1-45a1-aee1-4ae6cc436845" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe8_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0045">
            <matter xsi:type="esdl:Material" id="930aa5cf-b76e-4049-afa7-ea79445faf55" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.04385">
            <matter xsi:type="esdl:Material" id="f6bd7242-b1a3-4b24-9edd-ad58a830444b" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="81df81a9-ac8b-4c9d-8d71-dd2bbee92fa3" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe9_ret" name="Pipe9_ret" innerDiameter="0.3444" outerDiameter="0.5" length="53.2" diameter="DN350" related="Pipe9">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99916480455774" lon="4.367928468290946"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.999168262107005" lon="4.367938710740932"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.9994879036446" lon="4.368502661385395"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3c52ca3a-e59e-4fff-a451-fc110907d9aa" name="In_ret" connectedTo="c0bdb043-c1ec-455f-92f2-eabbbcb8580a" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="c52483a0-d143-4106-a43b-746311baefe2" name="Out_ret" connectedTo="8b9b3b28-f224-4642-8b37-f84fcf540c2e" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="74cb4f2f-49e8-4ffe-a9dd-e1761e1360fb" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="646e9c15-7318-420d-b6ca-716f75d37d8c" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="45d19676-c919-428a-b870-3f7c94a70776" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="aff47494-34ab-436e-a66c-76fc20d278d7" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe9_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="d2298eee-877b-45e1-8b67-cc63fc2f6c69" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0666">
            <matter xsi:type="esdl:Material" id="cd3d98cc-58f2-4683-8523-7e4183c7e685" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="3979c7f7-6acf-4a32-81bb-8ed118357c6b" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe11_ret" name="Pipe11_ret" innerDiameter="0.3444" outerDiameter="0.5" length="102.7" diameter="DN350" related="Pipe11">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.998285701083724" lon="4.368405699422867"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.999160108482904" lon="4.3679277752889245"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="03f16a92-b24d-4e11-b730-83b703517cad" name="In_ret" connectedTo="b57116bc-1f78-402c-84c0-fc6e5846cf8a" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="1207cf4b-308c-4466-b1c8-9e997e988fff" name="Out_ret" connectedTo="81a1bb4a-1701-4491-86d4-2c2f0b858aa2" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="889aaedb-0f1e-44d2-8c97-996efac54628" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="032dbbaf-0453-43e1-a99c-d9913ee944ed" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ec1869a2-2f79-4d7c-941d-667b920deeed" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="de74a14c-a30f-41d9-b566-95070ba2c66a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe11_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="d2298eee-877b-45e1-8b67-cc63fc2f6c69" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0666">
            <matter xsi:type="esdl:Material" id="cd3d98cc-58f2-4683-8523-7e4183c7e685" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0056">
            <matter xsi:type="esdl:Material" id="3979c7f7-6acf-4a32-81bb-8ed118357c6b" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe12_ret" name="Pipe12_ret" innerDiameter="0.263" outerDiameter="0.4" length="1695.06" diameter="DN250" related="Pipe12">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.98942341528986" lon="4.358033875102766"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.9896414426195" lon="4.358335460597678"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.990599428912915" lon="4.363308048432978"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99140544288403" lon="4.3656512071836415"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99175559197406" lon="4.367015611554548"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99205288622196" lon="4.369055647987936"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.992614436638156" lon="4.371890986540468"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.9964526103122" lon="4.369453529130539"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99698107661307" lon="4.369134268411443"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.998285701083724" lon="4.368405699422867"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="15cec74a-ff3d-4349-99c1-b63e54984020" name="In_ret" connectedTo="ba357584-609f-4cf2-aedd-0fac5c8ceade" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="a2336831-a837-4c16-8b13-5ccaf7ad4b28" name="Out_ret" connectedTo="9499403a-8dcf-4c77-944d-a56829b8ff7e" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="eada3e36-6ccb-4581-bbf5-894cc070f596" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="85cdbdcc-d786-46d3-a614-587ca770acdb" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="44a17566-7f6f-4068-bba2-8766c25885b4" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e7dbc828-0780-4b40-86dd-d97345e526ae" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe12_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.005">
            <matter xsi:type="esdl:Material" id="faac539b-4b7c-43f8-abcd-f08fa2652b7b" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0587">
            <matter xsi:type="esdl:Material" id="d23b4eeb-a419-4c16-bc7e-280a76116f04" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0048">
            <matter xsi:type="esdl:Material" id="a2b91e8d-471d-4276-a8f6-4efb01054b4e" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <asset xsi:type="esdl:Pipe" id="Pipe13_ret" name="Pipe13_ret" innerDiameter="0.2101" outerDiameter="0.315" length="285.9" diameter="DN200" related="Pipe13">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99937396000665" lon="4.3721244417482765"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.99922038334009" lon="4.371998986068785"/>
          <point xsi:type="esdl:Point" CRS="WGS84" lat="51.998285701083724" lon="4.368405699422867"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3e844e19-0eff-47e7-af3b-d95e29d0c7f8" name="In_ret" connectedTo="6a4e4835-ddee-4652-9cfa-2c8d49821d6f" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret"/>
        <port xsi:type="esdl:OutPort" id="b60cdb49-a624-4274-8daf-c769bc46d984" name="Out_ret" connectedTo="9499403a-8dcf-4c77-944d-a56829b8ff7e" carrier="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a96c52bd-5ef5-4713-83c0-4e36ed693ecd" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="HeatIn.Q">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6f4a2a5e-1ed5-4cda-b5cf-78a05fc52b0a" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="Heat_flow">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1222b22b-bca0-4c4d-b7f6-8b3d7784b2a2" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Velocity">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="834a9422-59a5-454e-8ac5-b7077f1b6231" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T23:00:00.000000+0000" host="localhost" port="8086" database="2f9e39d3-f62c-4f53-b670-e423c86ca0a0" filters="&quot;assetId&quot;='Pipe13_ret'" measurement="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" field="PostProc.Pressure"/>
        </port>
        <material xsi:type="esdl:CompoundMatter" compoundType="LAYERED">
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0045">
            <matter xsi:type="esdl:Material" id="930aa5cf-b76e-4049-afa7-ea79445faf55" name="steel" thermalConductivity="52.15"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.04385">
            <matter xsi:type="esdl:Material" id="f6bd7242-b1a3-4b24-9edd-ad58a830444b" name="PUR" thermalConductivity="0.027"/>
          </component>
          <component xsi:type="esdl:CompoundMatterComponent" layerWidth="0.0041">
            <matter xsi:type="esdl:Material" id="81df81a9-ac8b-4c9d-8d71-dd2bbee92fa3" name="HDPE" thermalConductivity="0.4"/>
          </component>
        </material>
      </asset>
      <KPIs xsi:type="esdl:KPIs" id="0eae1332-118a-48a7-8b4b-5f49cb4fb3d0">
        <kpi xsi:type="esdl:DistributionKPI" name="High level cost breakdown [EUR] (yearly averaged)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="CAPEX" value="3614677.445866666"/>
            <stringItem xsi:type="esdl:StringItem" label="OPEX" value="4808530.6500375"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="High level cost breakdown [EUR] (30.0 year period)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="CAPEX" value="108440323.37599997"/>
            <stringItem xsi:type="esdl:StringItem" label="OPEX" value="144255919.501125"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="Overall cost breakdown [EUR] (yearly averaged)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="Installation" value="3333.3333333333335"/>
            <stringItem xsi:type="esdl:StringItem" label="Investment" value="3611344.1125333323"/>
            <stringItem xsi:type="esdl:StringItem" label="Variable OPEX" value="158530.65003750048"/>
            <stringItem xsi:type="esdl:StringItem" label="Fixed OPEX" value="4650000.0"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="Overall cost breakdown [EUR] (30.0 year period)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="Installation" value="100000.0"/>
            <stringItem xsi:type="esdl:StringItem" label="Investment" value="108340323.37599997"/>
            <stringItem xsi:type="esdl:StringItem" label="Variable OPEX" value="4755919.501125014"/>
            <stringItem xsi:type="esdl:StringItem" label="Fixed OPEX" value="139500000.0"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="CAPEX breakdown [EUR] (30.0 year period)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="HeatingDemand"/>
            <stringItem xsi:type="esdl:StringItem" label="GeothermalSource" value="40800000.0"/>
            <stringItem xsi:type="esdl:StringItem" label="ResidualHeatSource" value="45100000.0"/>
            <stringItem xsi:type="esdl:StringItem" label="Pipe" value="22540323.376"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="OPEX breakdown [EUR] (yearly averaged)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="GeothermalSource" value="2872615.654542024"/>
            <stringItem xsi:type="esdl:StringItem" label="ResidualHeatSource" value="1935914.9954954765"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="OPEX breakdown [EUR] (30.0 year period)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="COST" unit="EURO"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="GeothermalSource" value="86178469.63626072"/>
            <stringItem xsi:type="esdl:StringItem" label="ResidualHeatSource" value="58077449.8648643"/>
          </distribution>
        </kpi>
        <kpi xsi:type="esdl:DistributionKPI" name="Energy production [Wh] (yearly averaged)">
          <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" unit="WATTHOUR"/>
          <distribution xsi:type="esdl:StringLabelDistribution">
            <stringItem xsi:type="esdl:StringItem" label="GeothermalSource_9684" value="71307827271.01196"/>
            <stringItem xsi:type="esdl:StringItem" label="WarmteLinQ" value="1989374436.9345725"/>
          </distribution>
        </kpi>
      </KPIs>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="9d77d097-2ad4-4028-8b65-a3f136507a07">
    <carriers xsi:type="esdl:Carriers" id="82fb7d85-2f43-484a-8730-0c65ea567781">
      <carrier xsi:type="esdl:HeatCommodity" name="Supply" id="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" name="Supply_ret" id="58d6d5fc-8a6a-4a4d-9a9e-5992e18fe772_ret" returnTemperature="50.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="25075c4d-b03e-4395-8e2b-20dc3d31282e">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" multiplier="MEGA" unit="WATT" description="Power in MW" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR" description="Energy in kWh" id="12c481c0-f81e-49b6-9767-90457684d24a"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
