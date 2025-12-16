<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1" description="" id="2ec3c62d-7292-4938-8930-3b539b737cc9" esdlVersion="v2507" version="7">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="500000.0" controlStrategy="5ffde54c-cce1-4b85-83cb-bf43e2700b05">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="e79f56b3-f362-47fa-b386-1c3645aa7e43" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="661d5ff0-c971-4357-b3ff-2760666fce6a" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="06802302-9f65-479c-b172-ae031c8a964d" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="4fbb517d-f99d-494d-9da9-ce2f79f95672" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="210f7bd3-9e1d-4d58-9c26-1fb49c99d432" name="Pipe_210f" length="50.06">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080827626584416" lon="5.181051807770204"/>
          <point xsi:type="esdl:Point" lat="52.08084400577248" lon="5.181783846709909"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="e79f56b3-f362-47fa-b386-1c3645aa7e43" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="cce7e14a-ed70-433f-819c-917291f49ba2" name="Out" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="24f8f6f2-18f0-4720-8d38-bb68b39bfcab"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="ccb8c290-f6af-40b9-a635-e9fd1a3eaf8e" name="Pipe_ccb8" length="1422.56">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.08084400577248" lon="5.181783846709909"/>
          <point xsi:type="esdl:Point" lat="52.0809330937331" lon="5.202600922529884"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="c0f6a59b-d35a-490d-88f4-f9d38086e41f" name="In" carrier="497f44b0-cfe3-4c87-862c-492f9339c261" connectedTo="20da6152-aa7b-4fec-995b-01ff979ba2a1"/>
        <port xsi:type="esdl:OutPort" id="06802302-9f65-479c-b172-ae031c8a964d" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="b40ca673-0f51-42d9-b409-4ed2a816ff2d" name="Joint_b40c">
        <port xsi:type="esdl:InPort" id="24f8f6f2-18f0-4720-8d38-bb68b39bfcab" name="In" connectedTo="cce7e14a-ed70-433f-819c-917291f49ba2 2ee81eb7-7b24-441c-9be6-85f7a124c231" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="20da6152-aa7b-4fec-995b-01ff979ba2a1" name="Out" connectedTo="c0f6a59b-d35a-490d-88f4-f9d38086e41f" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <geometry xsi:type="esdl:Point" lat="52.08084400577248" lon="5.181783846709909"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="9b1c0e73-2e58-4af6-878c-7e00530bf4d0" name="Pipe_9b1c" length="1421.88">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07985204364499" lon="5.2026438490533"/>
          <point xsi:type="esdl:Point" lat="52.07974924861767" lon="5.181837488920463"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4fbb517d-f99d-494d-9da9-ce2f79f95672" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="7aa48701-3e91-441e-beb1-241c266e6f53" name="Out" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="29514053-e67a-4077-889f-e5a0d5e45344"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="0b020eb9-74f2-4ddf-88c8-39e34b2428d2" name="Pipe_0b02" length="44.89">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07974924861767" lon="5.181837488920463"/>
          <point xsi:type="esdl:Point" lat="52.07974657394189" lon="5.181180587340451"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="86429e06-a858-430c-8978-1663f23d44b2" name="In" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934" connectedTo="bae37dc2-1cfb-45eb-a61e-10c0ca9cb681"/>
        <port xsi:type="esdl:OutPort" id="661d5ff0-c971-4357-b3ff-2760666fce6a" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Joint" id="90542837-65f9-4cc2-9f25-b24b147c177a" name="Joint_9054">
        <port xsi:type="esdl:InPort" id="29514053-e67a-4077-889f-e5a0d5e45344" name="In" connectedTo="7aa48701-3e91-441e-beb1-241c266e6f53" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="bae37dc2-1cfb-45eb-a61e-10c0ca9cb681" name="Out" connectedTo="86429e06-a858-430c-8978-1663f23d44b2 907ff2d5-6f0a-401e-99fe-e0b021fa0662" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <geometry xsi:type="esdl:Point" lat="52.07974924861767" lon="5.181837488920463"/>
      </asset>
      <asset xsi:type="esdl:HeatProducer" id="86d87e9c-6a38-4e63-9b37-8fb4b7859965" name="HeatProducer_86d8" power="3000000.0" controlStrategy="0d83da60-d869-45a7-b16c-d17bd72e59dc">
        <geometry xsi:type="esdl:Point" lat="52.081516674561456" lon="5.1795523307497335" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="2ee81eb7-7b24-441c-9be6-85f7a124c231" name="Out" connectedTo="24f8f6f2-18f0-4720-8d38-bb68b39bfcab" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="907ff2d5-6f0a-401e-99fe-e0b021fa0662" name="InPort" connectedTo="bae37dc2-1cfb-45eb-a61e-10c0ca9cb681" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
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
  </energySystemInformation>
  <services xsi:type="esdl:Services" id="dea9d335-956b-4302-afb4-24a95f99ddc6">
    <service xsi:type="esdl:PriorityStrategy" id="5ffde54c-cce1-4b85-83cb-bf43e2700b05" name="PriorityStrategy for HeatProducer_49c0" priority="1" energyAsset="49c089de-564b-41c9-a56b-c616757aa86e"/>
    <service xsi:type="esdl:PriorityStrategy" id="0d83da60-d869-45a7-b16c-d17bd72e59dc" name="PriorityStrategy for HeatProducer_86d8" priority="2" energyAsset="86d87e9c-6a38-4e63-9b37-8fb4b7859965"/>
  </services>
</esdl:EnergySystem>
