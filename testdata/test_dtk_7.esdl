<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1_test" description="" id="82bb78a8-79f8-4568-af47-1ade96fd622c" esdlVersion="v2507" version="15">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4ae37969-65a5-4d62-b084-ffebf1a0a4ea" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="bba78b1f-5a77-47b2-80af-0403bb589a9c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="0d733df9-a028-47ca-9814-df48b5429e41" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="57f3988f-4c64-4756-a424-4200c1083399" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="44cbe1f3-5290-43ea-8339-2c807b82e49c" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_supply_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c0ebd75c-fffb-4934-811c-431ebb3e90dc" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_supplied">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="1edce403-4778-45b3-8e06-246a6f44857c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c8805a07-6166-4e0a-879f-6fe2b686dd94" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ed79dbee-994e-4ac0-a181-007729f25e34" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b6f237f5-f272-47ed-89b2-85370dcb36e7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4f289f5a-0882-4c97-b769-d3a1f9765988" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='49c089de-564b-41c9-a56b-c616757aa86e'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf" connectedTo="9ce14c79-5195-4251-af2e-ce9201b09a90">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="21d6be96-b0ae-40e1-a4c5-606279b48b94" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="78dd4f86-10b3-4e1f-8004-e4fcbb685287" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b432d1ee-a6c4-431f-b8ae-2b1b30198ab7" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4ba0cfd3-4116-4542-b4fe-3448ee81004f" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11" connectedTo="375b8076-7c09-4131-a476-d4c56e7f919d">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a4370f4b-b19b-42d5-a0c7-3897d79f38be" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c6e256cb-4741-4766-9a00-57403f5a8e1b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="219a1e33-4a29-4a1e-b06d-258e26b8b157" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e60ffc23-7626-450a-888a-c3a137cad890" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3c8a63b7-7feb-4e31-8a2c-6b5499541046" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="heat_demand_set_point">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="194e2342-9327-464c-806d-31d80a2e9129" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='679190ec-48e5-4b5e-8c11-633dc1513c1f'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="heat_demand">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="ee215750-42c9-4b2e-bcfb-2f64bee3a4b5" name="Pipe_ee21" length="725.8">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.180552471544395"/>
          <point xsi:type="esdl:Point" lat="52.08071805993588" lon="5.1911736292393815"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b1404ea6-1e4e-4b55-8fc9-de78a0dd6ba0" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="04cbd37c-1d05-450e-8545-82b41bd60873" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="07a56496-92ba-4b37-9b47-cc7f636beb10" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="24dad27a-2dbc-4bcd-bcbe-5445d01e1f07" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="0c47d5f1-c637-4cf7-a663-6d376a661012" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="bd6a7f01-3755-473b-8a44-0e19ff07f05a" name="Out" connectedTo="589c5585-8471-4698-bf98-f0eef7256af6" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d3b92190-da68-4ea1-b209-c7bd0b07d450" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1a39f97a-c9b1-48e3-acb6-5e63dedf9369" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="dc114173-3e00-4006-8957-1217a2031f69" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1aca8d51-8e01-4f0d-a18c-802a78a79634" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e26829a7-ce99-4e4e-9476-c5272e018de4" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3c7c9ee8-cc1b-4506-bcda-310145a0656f" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="27ec0c83-30cc-413f-8ad0-b2dad70fe79d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="cf9d2b1d-ec95-4af6-b8c0-c5a30070259d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='ee215750-42c9-4b2e-bcfb-2f64bee3a4b5'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f32bde06-0156-47c7-9d2f-5072b411829f" name="Pipe_f32b" length="730.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07966286980711" lon="5.191216543007839"/>
          <point xsi:type="esdl:Point" lat="52.07958372954184" lon="5.180531014660167"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="54a7a58c-340d-4d8a-85d5-4e83de250b32" name="In" connectedTo="4e86f312-b071-4216-a183-8b1f37c15d07" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="4861ae87-2b09-4628-9ab1-9c6d1e301fa9" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d9179c2e-4f69-41bc-9546-36e8ae635ffe" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="53c23457-c419-4fa7-a7ba-3bf9b2961f7d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="2ee1e145-9077-4958-9beb-d2751a0d587e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ccf391d4-0370-472a-9b41-affb94567bbf" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="1edce403-4778-45b3-8e06-246a6f44857c" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="7811bfd7-75b4-46f1-9425-286856739ab9" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1548ab9d-5942-4206-a069-18d1117f8fa5" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="eeddddd2-aee9-4d35-b6b9-4569d40d340b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="360235ee-cca6-410c-8956-d83024cae9d2" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="d3df7eac-d58d-408f-a239-cb5443f939a9" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="velocity">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="SPEED" unit="METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="db8214c6-1f0c-4a96-af00-0fdcbbcf8520" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="06e7a54e-b761-4d05-b800-1cd757b6f4e6" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure_loss_per_length">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="a97bb722-3b38-4d53-b630-08232a40bbe8" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='f32bde06-0156-47c7-9d2f-5072b411829f'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_loss">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="POWER" unit="WATT"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="8854c9bb-399f-4b83-83d7-7ed9462f59bd" name="HeatPump_8854">
        <geometry xsi:type="esdl:Point" lat="52.08020600176749" lon="5.192075523692222" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="589c5585-8471-4698-bf98-f0eef7256af6" name="Prim_in" connectedTo="bd6a7f01-3755-473b-8a44-0e19ff07f05a" carrier="497f44b0-cfe3-4c87-862c-492f9339c261">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f59c217e-c393-471f-97c9-f9935ec0fa46" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="394aa9ff-6e8b-401f-acad-e976418c774d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f147d755-d863-4582-887b-d4e3934fca84" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="b1267c60-330a-44c4-9727-f47de4726b97" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="039b96af-5385-4c54-bbbe-bb7c2747b380" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="497f44b0-cfe3-4c87-862c-492f9339c261" field="heat_power_secondary">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="4e86f312-b071-4216-a183-8b1f37c15d07" name="Prim_out" connectedTo="54a7a58c-340d-4d8a-85d5-4e83de250b32" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="779d0fc3-e750-497d-a31a-b22f4d0350d3" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="ea982ee0-469a-4e2b-8fc4-8f5c47f50eef" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="c4dd8e2d-411e-44ec-81b7-37e2e518ea74" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3c4b7aa3-a16e-4c16-87e4-37bb1f13f301" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e690071c-c3e7-44d1-9971-4b9b37f64018" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="heat_power_primary">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f03da094-d485-49f7-89ed-55bb98c95508" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="b34bc6ff-0f30-48d9-8604-9e9db1e34934" field="electricity_consumption">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
          </profile>
        </port>
        <port xsi:type="esdl:InPort" id="9e01177a-9aca-402a-94a9-50f9c82999ae" name="Sec_in" connectedTo="2485b2e3-1069-4019-851b-188b68c1f411" carrier="7428fc2b-a79c-48dd-a417-4d09fb2ddbb7">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="f47c62a0-b5d5-44d6-b217-cfb082d27c0f" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="87601a06-7ecc-4f3c-879a-35958420c3e4" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e20c55b1-8959-46fd-bd08-c9bc08dd9a1e" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="8f76f1db-3688-447a-acff-0ee3b8af699d" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="7cd930ee-a18e-4783-a9cf-6d64bf298a11" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
        <port xsi:type="esdl:OutPort" id="45d1b11f-f190-4f0b-a7ec-f5f05e84b8bd" name="Sec_out" connectedTo="24e09983-b310-47c1-936a-35c74a1eea14" carrier="0aa425d7-b0f6-45e3-862e-9442e16af02d">
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="3a1ccc5c-47bf-48d1-a0e6-2e9ad60a5078" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="mass_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" multiplier="KILO" unit="GRAM" perTimeUnit="SECOND"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="e26919c2-3415-4592-9e68-6686d253f16f" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="pressure">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="PRESSURE" unit="PASCAL"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="1ffaa8f3-4cef-4805-834f-72c08c987862" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="temperature">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="TEMPERATURE" unit="KELVIN"/>
          </profile>
          <profile xsi:type="esdl:InfluxDBProfile" profileType="OUTPUT" id="43f53e91-31c4-481e-94d8-d5e531bf669b" startDate="2019-01-01T00:00:00.000000" endDate="2019-01-07T23:00:00.000000" host="omotes_influxdb" port="8096" database="82bb78a8-79f8-4568-af47-1ade96fd622c" filters="&quot;assetId&quot;='8854c9bb-399f-4b83-83d7-7ed9462f59bd'" measurement="baeed7a3-22e7-43b4-ad3b-837aa0634daf" field="volume_flow">
            <dataSource xsi:type="esdl:DataSourceReference" reference="449130e3-328e-47fe-a6dc-dc044aa5d7fe"/>
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" physicalQuantity="FLOW" unit="CUBIC_METRE" perTimeUnit="SECOND"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f47ecb68-368f-4735-bedc-324ea6283266" name="Pipe_f47e" length="233.2">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080726075596964" lon="5.192889090510896"/>
          <point xsi:type="esdl:Point" lat="52.08073925903416" lon="5.196301749123236"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="24e09983-b310-47c1-936a-35c74a1eea14" name="In" connectedTo="45d1b11f-f190-4f0b-a7ec-f5f05e84b8bd" carrier="0aa425d7-b0f6-45e3-862e-9442e16af02d"/>
        <port xsi:type="esdl:OutPort" id="b6e43ed7-1aa1-44f2-abbb-3890d35df376" name="Out" carrier="0aa425d7-b0f6-45e3-862e-9442e16af02d" connectedTo="4670deb8-34cf-41e6-ae4b-0d89c256836d"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="187faa87-d686-4386-a8aa-2607b73c0623" name="Pipe_187f" length="312.4">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08073925903416" lon="5.198136857999694"/>
          <point xsi:type="esdl:Point" lat="52.08073925903416" lon="5.202708532744543"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="94c3f89e-1996-4755-980f-76fa4f4ef0b1" name="In" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf" connectedTo="45a48417-aab6-4db5-b7ff-2b0caea9ec19"/>
        <port xsi:type="esdl:OutPort" id="9ce14c79-5195-4251-af2e-ce9201b09a90" name="Out" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="0cf1033c-4493-4954-97ea-25c612fc3468" name="Pipe_0cf1" length="324.2">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.079809817171366" lon="5.2028587755765185"/>
          <point xsi:type="esdl:Point" lat="52.07977026602449" lon="5.1981153947379655"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="375b8076-7c09-4131-a476-d4c56e7f919d" name="In" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26"/>
        <port xsi:type="esdl:OutPort" id="f2d02478-cb6f-4c6f-aa7a-ac186efbf7e6" name="Out" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11" connectedTo="448d87e9-65fa-443a-aa75-f6c18ecf3e56"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="cfcc6fff-9f17-4372-89e4-fed2e9972c1b" name="Pipe_cfcc" length="247.2">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.079763674163296" lon="5.19636613890838"/>
          <point xsi:type="esdl:Point" lat="52.07974389857379" lon="5.192749579309784"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="360649c0-7cfb-4751-94e1-8016879b7d5b" name="In" carrier="7428fc2b-a79c-48dd-a417-4d09fb2ddbb7" connectedTo="4c5ac2a3-0a16-417c-8f81-f6ef694949f3"/>
        <port xsi:type="esdl:OutPort" id="2485b2e3-1069-4019-851b-188b68c1f411" name="Out" connectedTo="9e01177a-9aca-402a-94a9-50f9c82999ae" carrier="7428fc2b-a79c-48dd-a417-4d09fb2ddbb7"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="232f1ca0-7e6a-457d-924a-1ba38fa91fc8" name="HeatPump_232f">
        <geometry xsi:type="esdl:Point" lat="52.080218510303624" lon="5.197192474484345" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="4670deb8-34cf-41e6-ae4b-0d89c256836d" name="PrimIn" connectedTo="b6e43ed7-1aa1-44f2-abbb-3890d35df376" carrier="0aa425d7-b0f6-45e3-862e-9442e16af02d"/>
        <port xsi:type="esdl:OutPort" id="4c5ac2a3-0a16-417c-8f81-f6ef694949f3" name="PrimOut" connectedTo="360649c0-7cfb-4751-94e1-8016879b7d5b" carrier="7428fc2b-a79c-48dd-a417-4d09fb2ddbb7"/>
        <port xsi:type="esdl:InPort" id="448d87e9-65fa-443a-aa75-f6c18ecf3e56" name="SecIn" connectedTo="f2d02478-cb6f-4c6f-aa7a-ac186efbf7e6" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="45a48417-aab6-4db5-b7ff-2b0caea9ec19" name="SecOut" connectedTo="94c3f89e-1996-4755-980f-76fa4f4ef0b1" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="HeatSupplyprim" supplyTemperature="50.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="HeatReturnprim" returnTemperature="40.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="baeed7a3-22e7-43b4-ad3b-837aa0634daf" name="HeatSupplysec" supplyTemperature="70.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="7cd930ee-a18e-4783-a9cf-6d64bf298a11" name="HeatReturnsec" returnTemperature="60.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="0aa425d7-b0f6-45e3-862e-9442e16af02d" name="HeatSupplyMid" supplyTemperature="59.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="7428fc2b-a79c-48dd-a417-4d09fb2ddbb7" name="HeatReturnMid" returnTemperature="55.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
    <dataSources xsi:type="esdl:DataSources" id="26e95c54-ca6d-45b5-b65e-286199571d0d">
      <dataSource xsi:type="esdl:DataSource" id="449130e3-328e-47fe-a6dc-dc044aa5d7fe" name="Omotes simulator core run" description="This profile is a simulation results obtained with the Omotes simulator core" reference="https://simulator-core.readthedocs.io/en/latest/" releaseDate="2025-12-16T15:04:31.467640" version="0.0.28" license="GNU GENERAL PUBLIC LICENSE" author="Deltares/TNO" contactDetails="https://github.com/Project-OMOTES"/>
    </dataSources>
  </energySystemInformation>
</esdl:EnergySystem>
