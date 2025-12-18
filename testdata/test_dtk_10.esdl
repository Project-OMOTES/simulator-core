<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1_test" description="" id="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" esdlVersion="v2507" version="5">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="06802302-9f65-479c-b172-ae031c8a964d" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="19561a8a-300d-40f3-bd58-a4e38b05e228" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="5318220e-09e8-4e02-aefd-acee24fde9e3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1728ba40-0264-4c49-aa17-51c75518cfa1" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="188f24c6-932d-43e4-b46f-3fdc0c685460" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="4fbb517d-f99d-494d-9da9-ce2f79f95672" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1bef3c37-ebfb-4d7b-95f5-eca2b7d175af" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f1207fa4-1e02-4dd9-875d-1114e4764ec7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="78debe73-2618-452a-8c2d-5808e7d79004" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="52edba52-9802-4064-a82b-86a2a375b796" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d10ec79f-7f8a-47d2-a998-6561eeaef77b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_demand_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="818a82cc-67e5-4967-8480-f289917d90cd" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_demand">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="edccf512-5468-465a-b7f6-a7786fc02efe" name="Pipe_edcc" length="1472.6">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080827626584416" lon="5.181051807770204"/>
          <point xsi:type="esdl:Point" lat="52.0809330937331" lon="5.202600922529884"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e79f56b3-f362-47fa-b386-1c3645aa7e43" name="In" connectedTo="00526e8b-cef5-4406-97fa-922443c37479" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="cd33ba23-b5ea-42c4-b26d-43b5a4be3d25" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8fbd260c-23ae-4337-99fa-e84535daa665" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c7b64791-ae16-40a7-a247-8076328d0911" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e690986c-dbb1-41d5-b91c-b5b21527759b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="99c435dd-9c54-4227-97ac-6a05fe0066f6" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="06802302-9f65-479c-b172-ae031c8a964d" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="7e0cb958-202c-4f6d-8f2a-fe98c06eb61e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3f3baa6d-4edb-49f5-a292-d6bc6c038e2a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="feeca3b5-e7ab-4bdc-9376-36d2acdfd14c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9da3c166-6ce0-461d-a933-0d360630346b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="395bbcdb-d730-4368-8c2e-34ca33d242db" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b8cd898e-0758-49fd-b874-86ad69759005" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="0ca82c6e-3173-4569-bd2b-77a98e674b75" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b5998ac1-646d-4643-bea6-41fa5ccabc19" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='edccf512-5468-465a-b7f6-a7786fc02efe'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="e2d1f452-43f0-4e52-853c-c3ab5ec3f320" name="Pipe_e2d1" length="1466.8">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07985204364499" lon="5.2026438490533"/>
          <point xsi:type="esdl:Point" lat="52.07974657394189" lon="5.181180587340451"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4fbb517d-f99d-494d-9da9-ce2f79f95672" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="debc1eeb-8cc9-4d5a-a3cb-f666721d5972" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a0c95a07-d968-4146-bdcf-a1e269859cfc" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="14144836-b33e-4be1-b56f-8d76145c3513" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="971eeed7-232d-4606-8d95-3abc9caa1606" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="9af2534e-e899-4eb7-8407-428ee2f5059a" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="661d5ff0-c971-4357-b3ff-2760666fce6a" name="Out" connectedTo="84049736-f3ec-40f9-999b-fcc20dbb9d49" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e861654b-2e38-452c-b60c-406d994f137b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="333acca1-b844-4490-8454-adb73975f4e7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e046c2d6-7208-4b2e-8898-26d582dba5a3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6f0ca2a8-cdf9-46f5-9d67-37525fc38f1d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="508730e1-4e99-46fb-99a0-c64aacd152d8" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="de95f418-3adf-4363-a64a-2ed50f3e6e53" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="73969f2e-8bda-4c42-8ed0-b375481fa5e9" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d825e05a-2d6f-47df-bbdb-4cdc8c7ff0a6" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='e2d1f452-43f0-4e52-853c-c3ab5ec3f320'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="af1855c5-fd34-4ee1-a821-29cbf95b4a12" name="HeatPump_af18" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08023066970483" lon="5.180410610452403" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="84049736-f3ec-40f9-999b-fcc20dbb9d49" name="In" connectedTo="661d5ff0-c971-4357-b3ff-2760666fce6a" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="502cbc90-1b69-4c44-b5c8-42cda99c9479" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1e9706ae-8288-45e2-b656-e530a62c8344" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8bcf7dfc-fc46-4524-b31c-aaae39bc385c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c0e81792-e1f8-49b9-ad77-5d130706748e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="00526e8b-cef5-4406-97fa-922443c37479" name="Out" connectedTo="e79f56b3-f362-47fa-b386-1c3645aa7e43" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="7f6b8d31-1f42-4e31-a70d-6d0927ad2a53" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="6141cf0c-3050-4a49-99ee-480895c379d1" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="beb70eff-1c22-4e44-97c9-ba1bce7c7536" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="fe76312e-d10e-4808-9ecc-44421c4cdb44" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="738eb9b5-1c42-4634-9375-132d7b881450" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_supply_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="db1c4ea4-daac-4285-885a-c91fe62e57c1" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_supplied">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="74945736-a65a-46fc-af3f-658c579fbe38" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="e59e6487-39c4-48f8-a68b-8e1fc56f5a48" filters="&quot;assetId&quot;='af1855c5-fd34-4ee1-a821-29cbf95b4a12'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="electricity_consumption">
            <dataSource xsi:type="esdl:DataSourceReference" reference="105028a5-5a02-4e4a-b715-a071629ff106"/>
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
    <dataSources xsi:type="esdl:DataSources" id="2f12c1a8-6d70-4beb-ad22-9b1c256133d5">
      <dataSource xsi:type="esdl:DataSource" id="105028a5-5a02-4e4a-b715-a071629ff106" name="Omotes simulator core run" description="This profile is a simulation results obtained with the Omotes simulator core" reference="https://simulator-core.readthedocs.io/en/latest/" releaseDate="2025-12-17T14:31:15.295001" version="0.0.28" license="GNU GENERAL PUBLIC LICENSE" author="Deltares/TNO" contactDetails="https://github.com/Project-OMOTES"/>
    </dataSources>
  </energySystemInformation>
</esdl:EnergySystem>
