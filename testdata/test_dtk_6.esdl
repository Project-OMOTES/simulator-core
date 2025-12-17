<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1_test 6" description="" id="723ddd78-7b45-489c-bfc4-c74caeeea5c5" esdlVersion="v2507" version="6">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="e79f56b3-f362-47fa-b386-1c3645aa7e43" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="41a5e8c1-765c-4320-ac4b-2b1537d350dd" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9e613904-1b48-4fb0-bfee-eb6a15e5fe3e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8a5d9589-769f-4216-8d78-c9a9c4b0d514" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a4f62a75-7374-4fb2-b4b9-81220c3e1afd" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e8f9e17c-df5a-4b8b-9131-065e661c8af3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_supply_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d0534f04-a499-462a-8f74-913f4e5da1f3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_supplied">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="661d5ff0-c971-4357-b3ff-2760666fce6a" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="73d1c8f6-8c68-4ddb-87b3-81c227c30a32" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="89b13019-d751-428c-9b6b-6d6458300d1d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1ddb7296-88c0-47bb-8845-4bee1edd9443" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="10d434bf-5a45-44f4-b689-a7c7a1a94789" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="06802302-9f65-479c-b172-ae031c8a964d" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="23b133f2-e517-487b-a613-9a2803f28800" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="fd1120da-6f80-40a5-8696-2b516680d809" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ad12371b-8c9d-44a7-8215-56486f35f466" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="160d1826-5e58-4fc6-a940-430a016e1ae1" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="4fbb517d-f99d-494d-9da9-ce2f79f95672" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f955ff5d-e7dc-4ea2-a61b-43c220c9ebd9" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9d819849-78f4-4fba-ae52-3f5a2528ba2c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="951a4385-9eb8-4383-8933-bf78dc8ed77e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ebd25cf1-bb93-42c5-be75-938c441baec5" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="88a2ac28-9e58-4cf8-bc6e-798fc2857ab7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_demand_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c7696379-cf16-4f1b-9b5f-b3079bfc2b60" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_demand">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="91d9da3b-06cf-452d-ae82-4a6824a230d9" name="HeatingDemand_91d9">
        <geometry xsi:type="esdl:Point" lat="52.07825320355558" lon="5.2036357205443995"/>
        <port xsi:type="esdl:InPort" id="57103993-7189-452d-b454-0872fd390efd" name="In" connectedTo="29254d67-3900-47a9-89ce-e1659eca8fa6" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e7d49c00-0d24-4939-b746-b4b3caf807a7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a52096e8-e397-4fb7-83e8-74b7c9c7c91e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d67a8077-bcbb-43fa-8b5d-ed4230f4834a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c2b86c19-8a80-4a00-924a-5d74ff2c6d2b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="04d03d78-5895-478f-8b7b-9fbf112fa83d" name="Out" connectedTo="ca11d672-5f04-4a2a-b60c-fbaeb15cb7fc" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="842f9357-4c49-4592-9233-fd663a8af213" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="7138ef0a-405d-412b-aa17-7e5f26585132" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5d830672-c467-46b3-ae93-5e8de262ef2d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5e60550d-d810-431b-ab4b-9130349e6116" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="65a97ee2-a4b1-44aa-9793-2ba2cfbf6901" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d2f0a762-dd38-4f4b-88dd-b1728cc8bb45" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_demand_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="965ebe4e-a730-4777-972b-96899a7e068a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='91d9da3b-06cf-452d-ae82-4a6824a230d9'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_demand">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="faf86c4f-6cac-4873-8a32-fa1063ae19bb" name="Pipe_faf8" length="1364.82">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080827626584416" lon="5.181051807770204"/>
          <point xsi:type="esdl:Point" lat="52.080930964801496" lon="5.201023708341551"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e79f56b3-f362-47fa-b386-1c3645aa7e43" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a16f53f3-389f-4544-b66e-75d57eba3191" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c376ccd9-6c6e-4cdd-b095-3c050c956842" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="89c81c9e-dfb1-4012-8b8a-eac141692553" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="01df6aca-ce9a-4e39-a934-f04349fd6f39" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c6febb58-011d-4e7b-af8c-dc3cd8833e8b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="7f78aa63-51f2-4f1f-8357-293279d03dcd" name="Out" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="08abd36a-ad8b-469d-afb5-4b46d9836bdc">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9a9d6222-ba6f-404a-b7b6-76912329c36e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c85b80ff-e2fe-4f25-bbce-0cfc4730782a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c5687eb2-2284-402a-99f2-823ca2db3739" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="48c1bd67-b06f-4f27-a622-1b8499d01f52" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="592825a1-f947-440d-92c7-ff57848829d3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f0b98f64-0b61-4c1c-a1a5-a632ead5cf4b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f9e3a716-0870-48b0-af93-6fadef55744a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="783741ed-9e07-4599-a516-db5f2fc9a867" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='faf86c4f-6cac-4873-8a32-fa1063ae19bb'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20" name="Pipe_80ae" length="107.78">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080930964801496" lon="5.201023708341551"/>
          <point xsi:type="esdl:Point" lat="52.0809330937331" lon="5.202600922529884"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="3a37954f-0610-4297-a49d-aaa4d2f50a6f" name="In" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="fb5a84c0-457a-4c88-b8a4-c539a35cbc44">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="60dd1817-4dfd-4277-816a-57363bd21f44" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="bcbfa956-05b2-4572-ab12-e7cd850e8dc7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="278c6e2a-2e0a-4965-83dd-5505dd428ae6" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="948e05c3-4d0e-4c18-a568-50c55b65c1fe" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6f31717c-8a5a-4b50-84b2-cf1ad8444508" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="06802302-9f65-479c-b172-ae031c8a964d" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ae7d68bc-87fa-4fa3-bca4-7b2f10941666" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8fab52fb-bd54-4b71-8c8e-deba31cd8c52" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3bea4666-35b8-4f30-a73f-ea8da0520990" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="0c93e1a5-b60f-42b0-956b-62e14db1bea2" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="62d969cf-8ab8-4fa0-bdd7-980d79ad052e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="14738632-c48e-4459-b370-5f124e104e3c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="58ac8ad4-4140-493f-b114-9c6be7adef22" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="526ec450-0d2f-4a7e-b2fe-c38b5a457b67" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='80aecf1b-dff1-4d2b-a5a5-f1bfd8311a20'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="e2cdbed0-bc6e-4c7e-b2b2-d2b7da88f68a" name="Joint_e2cd">
        <port xsi:type="esdl:InPort" id="08abd36a-ad8b-469d-afb5-4b46d9836bdc" name="In" connectedTo="7f78aa63-51f2-4f1f-8357-293279d03dcd" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="fb5a84c0-457a-4c88-b8a4-c539a35cbc44" name="Out" connectedTo="3a37954f-0610-4297-a49d-aaa4d2f50a6f 81273ed5-e24f-438e-867d-34717c82a633" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <geometry xsi:type="esdl:Point" lat="52.080930964801496" lon="5.201023708341551"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="158408e1-eb50-4cf2-8898-a93fbca8bbf1" name="Pipe_1584" length="178.19">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07985204364499" lon="5.2026438490533"/>
          <point xsi:type="esdl:Point" lat="52.0798630983578" lon="5.200036398302746"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4fbb517d-f99d-494d-9da9-ce2f79f95672" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="16863675-e180-46ab-a281-db268f714807" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="58ab5957-350c-4f25-8211-d350ead67fd8" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9b464555-226e-40ed-ac79-e801a177e061" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="09281984-1398-4a5d-a2d2-99f503ada586" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="557d7a7a-37f8-4260-bdc3-af1aca25e8c4" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="94f02cd0-9b43-4fc7-8c35-a2d8f0aeb630" name="Out" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="34db3c81-959b-4179-a27f-410349b196c5">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3274dea1-e3ba-4926-90f5-88b275a7011b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="14e18175-2cec-4eca-abd9-aa899b314509" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="694d8e5f-8bf7-4f3f-b8b8-6cf012033c1d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c9c97e2d-88d8-4ca0-b162-165dfbf309d0" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ae1ecac1-71f2-4880-b8dd-d4a119910a97" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b41aa092-c1d3-4680-a95a-cf09a446e3f8" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4c8016ee-d6e6-47d3-80ce-ef7900cdd600" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e9de123c-02c5-4bf3-bae9-4c906b359913" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='158408e1-eb50-4cf2-8898-a93fbca8bbf1'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="7f23dc6f-e9c9-490b-ba77-01b1b02541ee" name="Pipe_7f23" length="1288.6">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.0798630983578" lon="5.200036398302746"/>
          <point xsi:type="esdl:Point" lat="52.07974657394189" lon="5.181180587340451"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="1945e546-631e-4748-9981-63454520e872" name="In" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="c478c49f-c8a1-4aa3-912d-27e4cd5929a9">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="0e77f263-721d-4c7f-8622-b18ec7a4eefd" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="bac6ff80-40d3-4026-8641-4ce3f6b54abd" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a6ab2f33-fe6a-4ce5-960d-d384b13c4fe8" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="41dea5a5-7769-4171-87b5-6fd906b87e62" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5e5bc19e-88fb-4fb0-8b3f-b390497e86e9" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="661d5ff0-c971-4357-b3ff-2760666fce6a" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="71023429-e306-4b63-b65a-2164e4024d8d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="35f108da-635e-4396-b14a-474b5bda7510" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f4fea58f-462e-4fa1-9dfb-eccb66f7cb3e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4a18a912-9e51-49ca-80c2-fc1c7260bcbc" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b335a002-0301-4d48-85ae-5729d4afa7e1" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c0396ec8-a259-447e-8181-ebc5e757fc38" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4ce57d42-ed6f-4002-a3f4-56b15cc18685" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="801d1c3d-3547-48be-86ea-fe3ea376e720" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='7f23dc6f-e9c9-490b-ba77-01b1b02541ee'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Joint" id="0ede0bba-b350-419e-8d90-0b7451f61066" name="Joint_0ede">
        <port xsi:type="esdl:InPort" id="34db3c81-959b-4179-a27f-410349b196c5" name="In" connectedTo="94f02cd0-9b43-4fc7-8c35-a2d8f0aeb630 d3c997f8-3a3e-4256-b457-aeb7512ee236" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="c478c49f-c8a1-4aa3-912d-27e4cd5929a9" name="Out" connectedTo="1945e546-631e-4748-9981-63454520e872" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <geometry xsi:type="esdl:Point" lat="52.0798630983578" lon="5.200036398302746"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="10858cd3-4b50-4353-8be1-a600e6e2e59e" name="Pipe_1085" length="272.7">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080627746062866" lon="5.200980781818095"/>
          <point xsi:type="esdl:Point" lat="52.07817555362053" lon="5.201002245079823"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="81273ed5-e24f-438e-867d-34717c82a633" name="In" connectedTo="fb5a84c0-457a-4c88-b8a4-c539a35cbc44" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="42b24b97-3c3c-4554-a7dc-e9cabc40c95d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f962a9a3-89e7-4022-ad27-b444177c1a99" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="07d213f9-31b3-49e4-b465-96e1b39e151a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="da515d57-f562-4fa9-b92b-79e9b0f1c73e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="bafec32d-846c-4903-a4b8-a49c25a8f284" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="29254d67-3900-47a9-89ce-e1659eca8fa6" name="Out" connectedTo="57103993-7189-452d-b454-0872fd390efd" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8f8fe9bb-fe11-4a36-9d07-ab0660fc384d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f208b451-35d1-4e12-9028-c5340908c3e3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="32168a76-6599-40fe-9bf6-b97f3eb2de59" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="0aea8949-cac8-4ab4-9806-0c473835b10b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="be794a62-d0cd-42b0-a520-bbc715066a12" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="515c66e2-f9e4-47f0-aea5-b49887da3e28" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5958d5ef-0cad-484e-9467-4276a5415f8c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="34b76d97-2a22-4438-ac03-62f03803c065" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='10858cd3-4b50-4353-8be1-a600e6e2e59e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="b7f143e1-b32a-4a63-96c9-a9d2cbbdea02" name="Pipe_b7f1" length="124.6">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.078558100138785" lon="5.199995383420375"/>
          <point xsi:type="esdl:Point" lat="52.07967873282826" lon="5.200038309943791"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="ca11d672-5f04-4a2a-b60c-fbaeb15cb7fc" name="In" connectedTo="04d03d78-5895-478f-8b7b-9fbf112fa83d" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4de0e2b4-27fb-4166-b7a0-23b6890bab91" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d8ffb621-aeba-4735-a57c-2975d536ba7f" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f80bd7c9-d47f-4bf1-bda9-da79c2d4e571" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ddb76a0a-6247-49d1-9040-46e7fa32e6a3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3260ec1a-4a6e-47ec-ad80-8b0c7493b1b6" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="d3c997f8-3a3e-4256-b457-aeb7512ee236" name="Out" connectedTo="34db3c81-959b-4179-a27f-410349b196c5" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="eb0bae0f-0c83-4c77-afa0-b972f3d3836b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5e59e5e6-122f-492b-b7b1-d44aa54978b1" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5412096f-221d-451f-ae60-fe9469eb1b23" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d4bd94bd-0664-4e64-bb40-9e8750609b8b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d1c9463c-7f49-40a1-8d78-89070b882c59" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1375ea48-1ddd-4490-89c4-ee7de2c02601" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="470d2f9b-08e4-4ab3-9a5e-bbbbb6a15b43" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4c9032e6-35da-4a6f-89d4-90b519c8625e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="723ddd78-7b45-489c-bfc4-c74caeeea5c5" filters="&quot;assetId&quot;='b7f143e1-b32a-4a63-96c9-a9d2cbbdea02'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="Supply" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="Return" returnTemperature="50.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
    <dataSources xsi:type="esdl:DataSources" id="d39ad944-7852-4c49-91e1-19d6b6594cdb">
      <dataSource xsi:type="esdl:DataSource" id="5e9fe5dd-a48b-482f-8b8f-b06b0a7ca9b6" name="Omotes simulator core run" description="This profile is a simulation results obtained with the Omotes simulator core" reference="https://simulator-core.readthedocs.io/en/latest/" releaseDate="2025-12-16T08:46:24.869192" version="0.0.28" license="GNU GENERAL PUBLIC LICENSE" author="Deltares/TNO" contactDetails="https://github.com/Project-OMOTES"/>
    </dataSources>
  </energySystemInformation>
</esdl:EnergySystem>
