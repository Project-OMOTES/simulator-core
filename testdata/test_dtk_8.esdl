<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1" description="" id="2ec3c62d-7292-4938-8930-3b539b737cc9" esdlVersion="v2507" version="12">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="1edce403-4778-45b3-8e06-246a6f44857c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" connectedTo="bdb2aa14-f978-4063-b314-4de861295e1b" carrier="35f0c30e-a4f3-4e13-8475-0448a4d3b12c"/>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" connectedTo="140fdf3b-c5af-4b2b-838d-b6c4cceb39b4" carrier="559d9a88-37a8-4172-815d-71300f2f6b12">
          <profile xsi:type="esdl:InfluxDBProfile" measurement="WarmingUp default profiles" field="demand4_MW" host="https://profiles.warmingup.info" database="energy_profiles" filters="" startDate="2018-12-31T23:00:00.000000+0000" endDate="2019-12-31T22:00:00.000000+0000" id="ae209104-2a72-4dea-a01c-1083c2de5c76" profileType="INPUT">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitReference" reference="e9405fc8-5e57-4df5-8584-4babee7cdf1b"/>
          </profile>
        </port>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="db270abe-fe5b-45e5-a9a3-ef3bef61b72b" name="HeatExchange_db27" capacity="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08017726075351" lon="5.192096279200813" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="b40c0fb5-5e07-4568-a13c-7549d0bb3913" name="PrimIn" connectedTo="bd6a7f01-3755-473b-8a44-0e19ff07f05a" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="8c109b7c-61f9-4913-a23b-7490f0296054" name="SecOut" connectedTo="9cd7d49a-9192-4109-accf-890d4b647dcd" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:InPort" id="fafdd706-b147-4d9a-a04f-c3c7bda8e1a2" name="SecIn" connectedTo="3a6aaa9a-e7b1-4b2c-ba08-5408e3171fc9" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="5efae14e-42f7-498f-b768-3cf9437f5710" name="PrimOut" connectedTo="54a7a58c-340d-4d8a-85d5-4e83de250b32" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="ee215750-42c9-4b2e-bcfb-2f64bee3a4b5" name="Pipe_ee21" length="725.8">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.180552471544395"/>
          <point xsi:type="esdl:Point" lat="52.08071805993588" lon="5.1911736292393815"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" name="In" connectedTo="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="bd6a7f01-3755-473b-8a44-0e19ff07f05a" name="Out" connectedTo="b40c0fb5-5e07-4568-a13c-7549d0bb3913" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="f32bde06-0156-47c7-9d2f-5072b411829f" name="Pipe_f32b" length="730.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07966286980711" lon="5.191216543007839"/>
          <point xsi:type="esdl:Point" lat="52.07958372954184" lon="5.180531014660167"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="54a7a58c-340d-4d8a-85d5-4e83de250b32" name="In" connectedTo="5efae14e-42f7-498f-b768-3cf9437f5710" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:OutPort" id="1edce403-4778-45b3-8e06-246a6f44857c" name="Out" connectedTo="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="52270727-96fc-42bf-b227-dadd208ce6b6" name="HeatExchange_5227">
        <geometry xsi:type="esdl:Point" lat="52.08017962441516" lon="5.198880931562258" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="1667b4a1-f832-4e4c-aefc-d95d372cd3ae" name="PrimIn" connectedTo="a6928e10-42bf-4043-b0b9-131a05fed9d3" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="9e38cfe5-3f1c-47c8-a417-f183526c95fb" name="PrimOut" connectedTo="6c5117f8-fae2-46ce-8242-cdb0f9418ea6" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:InPort" id="225aa162-9390-4e8f-84c3-417fb1e08b1e" name="SecIn" connectedTo="67ae3854-25ec-4f56-9ee5-ab5cbef9b05b" carrier="559d9a88-37a8-4172-815d-71300f2f6b12"/>
        <port xsi:type="esdl:OutPort" id="f91012c7-e66d-47c2-91cc-023b6cdc103f" name="SecOut" connectedTo="01b74c0f-3907-4d82-83c7-b011d080f2cd" carrier="35f0c30e-a4f3-4e13-8475-0448a4d3b12c"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="50513f3c-8974-4b2b-9159-5c67629ba2f5" name="Pipe_5051" length="316.8">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08074651563915" lon="5.193279020255189"/>
          <point xsi:type="esdl:Point" lat="52.08073333220409" lon="5.197915084785182"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="9cd7d49a-9192-4109-accf-890d4b647dcd" name="In" connectedTo="8c109b7c-61f9-4913-a23b-7490f0296054" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="a6928e10-42bf-4043-b0b9-131a05fed9d3" name="Out" connectedTo="1667b4a1-f832-4e4c-aefc-d95d372cd3ae" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="1296caac-a8e7-45c4-960f-222cf9eb513f" name="Pipe_1296" length="222.9">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08078606592099" lon="5.1994819028902"/>
          <point xsi:type="esdl:Point" lat="52.08078606592099" lon="5.2027443186705655"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="01b74c0f-3907-4d82-83c7-b011d080f2cd" name="In" connectedTo="f91012c7-e66d-47c2-91cc-023b6cdc103f" carrier="35f0c30e-a4f3-4e13-8475-0448a4d3b12c"/>
        <port xsi:type="esdl:OutPort" id="bdb2aa14-f978-4063-b314-4de861295e1b" name="Out" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba" carrier="35f0c30e-a4f3-4e13-8475-0448a4d3b12c"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="59436ef1-5141-4b4b-af61-85af5af1b8e5" name="Pipe_5943" length="223.0">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.079625909757326" lon="5.202787245193981"/>
          <point xsi:type="esdl:Point" lat="52.07966546103211" lon="5.199524829413656"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="140fdf3b-c5af-4b2b-838d-b6c4cceb39b4" name="In" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26" carrier="559d9a88-37a8-4172-815d-71300f2f6b12"/>
        <port xsi:type="esdl:OutPort" id="67ae3854-25ec-4f56-9ee5-ab5cbef9b05b" name="Out" connectedTo="225aa162-9390-4e8f-84c3-417fb1e08b1e" carrier="559d9a88-37a8-4172-815d-71300f2f6b12"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="5bb9d02e-8392-4dae-83fb-ff19627a68cb" name="Pipe_5bb9" length="321.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07971819601064" lon="5.197936548046869"/>
          <point xsi:type="esdl:Point" lat="52.07966546103211" lon="5.193236093731773"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="6c5117f8-fae2-46ce-8242-cdb0f9418ea6" name="In" connectedTo="9e38cfe5-3f1c-47c8-a417-f183526c95fb" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="3a6aaa9a-e7b1-4b2c-ba08-5408e3171fc9" name="Out" connectedTo="fafdd706-b147-4d9a-a04f-c3c7bda8e1a2" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="Supply" supplyTemperature="80.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="Return" returnTemperature="50.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="baeed7a3-22e7-43b4-ad3b-837aa0634daf" name="SecSupply" returnTemperature="75.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="7cd930ee-a18e-4783-a9cf-6d64bf298a11" name="SecReturn" returnTemperature="55.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="35f0c30e-a4f3-4e13-8475-0448a4d3b12c" name="SecSupply2" supplyTemperature="70.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="559d9a88-37a8-4172-815d-71300f2f6b12" name="SecReturn2" returnTemperature="60.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
