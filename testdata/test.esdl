<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1" description="" id="2ec3c62d-7292-4938-8930-3b539b737cc9" esdlVersion="v2507" version="11">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="1edce403-4778-45b3-8e06-246a6f44857c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="2f79d5b2-9a60-4a1d-aab9-034937d9f7bf" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="0484020b-3fae-48d1-89b5-d37bc1095cb4" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:Pipe" id="ee215750-42c9-4b2e-bcfb-2f64bee3a4b5" name="Pipe_ee21" length="725.8">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.180552471544395"/>
          <point xsi:type="esdl:Point" lat="52.08071805993588" lon="5.1911736292393815"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="bd6a7f01-3755-473b-8a44-0e19ff07f05a" name="Out" connectedTo="589c5585-8471-4698-bf98-f0eef7256af6" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f32bde06-0156-47c7-9d2f-5072b411829f" name="Pipe_f32b" length="730.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07966286980711" lon="5.191216543007839"/>
          <point xsi:type="esdl:Point" lat="52.07958372954184" lon="5.180531014660167"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="54a7a58c-340d-4d8a-85d5-4e83de250b32" name="In" connectedTo="4e86f312-b071-4216-a183-8b1f37c15d07" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="1edce403-4778-45b3-8e06-246a6f44857c" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="fccedfe7-cbdd-459d-b8e2-e290fc261705" name="Pipe_fcce" length="695.1">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07972881992095" lon="5.2031036568725195"/>
          <point xsi:type="esdl:Point" lat="52.07962329969199" lon="5.19293309374643"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="0484020b-3fae-48d1-89b5-d37bc1095cb4" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="2fa55afc-fa8c-4ce6-8ea4-c76de866cdd5" name="Out" connectedTo="9e01177a-9aca-402a-94a9-50f9c82999ae" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="6cc85e36-c168-4ec1-971c-8d6123822e8b" name="Pipe_6cc8" length="683.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.192890179977971"/>
          <point xsi:type="esdl:Point" lat="52.0807708187875" lon="5.202889088030225"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="8d79c71e-8c27-4c6e-afa2-eeda757964bb" name="In" connectedTo="45d1b11f-f190-4f0b-a7ec-f5f05e84b8bd" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="2f79d5b2-9a60-4a1d-aab9-034937d9f7bf" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
      <asset xsi:type="esdl:HeatPump" id="8854c9bb-399f-4b83-83d7-7ed9462f59bd" name="HeatPump_8854">
        <geometry xsi:type="esdl:Point" lat="52.08020600176749" lon="5.192075523692222" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="589c5585-8471-4698-bf98-f0eef7256af6" name="Prim_in" connectedTo="bd6a7f01-3755-473b-8a44-0e19ff07f05a" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="4e86f312-b071-4216-a183-8b1f37c15d07" name="Prim_out" connectedTo="54a7a58c-340d-4d8a-85d5-4e83de250b32" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:InPort" id="9e01177a-9aca-402a-94a9-50f9c82999ae" name="Sec_in" connectedTo="2fa55afc-fa8c-4ce6-8ea4-c76de866cdd5" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="45d1b11f-f190-4f0b-a7ec-f5f05e84b8bd" name="Sec_out" connectedTo="8d79c71e-8c27-4c6e-afa2-eeda757964bb" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="HeatSupplyprim" supplyTemperature="30.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="HeatReturnprim" returnTemperature="20.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="baeed7a3-22e7-43b4-ad3b-837aa0634daf" name="HeatSupplysec" supplyTemperature="70.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="7cd930ee-a18e-4783-a9cf-6d64bf298a11" name="HeatReturnsec" returnTemperature="50.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
