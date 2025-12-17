<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="test_dtk_1" description="" id="2ec3c62d-7292-4938-8930-3b539b737cc9" esdlVersion="v2507" version="14">
  <instance xsi:type="esdl:Instance" id="0a0a7858-0829-4a90-9f36-7ceed8db0438" name="Untitled instance">
    <area xsi:type="esdl:Area" id="991ab0e1-be78-4111-8e39-03592e5cc2c6" name="Untitled area">
      <asset xsi:type="esdl:HeatProducer" id="49c089de-564b-41c9-a56b-c616757aa86e" name="HeatProducer_49c0" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.080168451259" lon="5.17963523249716" CRS="WGS84"/>
        <port xsi:type="esdl:OutPort" id="8a6e5449-8f08-4ce4-956c-cedf9c9b8a4e" name="Out" connectedTo="4eed84a0-5bba-4a34-8374-4fe4c82c91e4" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:InPort" id="31cc21ee-e4db-4cd0-8493-6ddb69d3442c" name="InPort" connectedTo="1edce403-4778-45b3-8e06-246a6f44857c" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
      </asset>
      <asset xsi:type="esdl:HeatingDemand" id="679190ec-48e5-4b5e-8c11-633dc1513c1f" name="HeatingDemand_6791" power="5000000.0">
        <geometry xsi:type="esdl:Point" lat="52.08019481845893" lon="5.203545306045233" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="850a4675-0c79-4b3a-9562-c8ae275b88ba" name="In" carrier="092a45a6-b26d-46bb-a84e-72d5bdb6807c" connectedTo="b44203fe-8a7e-4f23-8242-34646d2ca97f"/>
        <port xsi:type="esdl:OutPort" id="efcf3749-bb0d-4697-8d87-e39fae365c26" name="OutPort" carrier="b589726f-3940-4a1f-b06c-488862a9c4c6" connectedTo="a4bb1e29-342b-40b8-9794-2ffaa83dc18e">
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
      <asset xsi:type="esdl:HeatPump" id="8854c9bb-399f-4b83-83d7-7ed9462f59bd" name="HeatPump_8854">
        <geometry xsi:type="esdl:Point" lat="52.08020600176749" lon="5.192075523692222" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="589c5585-8471-4698-bf98-f0eef7256af6" name="Prim_in" connectedTo="bd6a7f01-3755-473b-8a44-0e19ff07f05a" carrier="497f44b0-cfe3-4c87-862c-492f9339c261"/>
        <port xsi:type="esdl:OutPort" id="4e86f312-b071-4216-a183-8b1f37c15d07" name="Prim_out" connectedTo="54a7a58c-340d-4d8a-85d5-4e83de250b32" carrier="b34bc6ff-0f30-48d9-8604-9e9db1e34934"/>
        <port xsi:type="esdl:InPort" id="9e01177a-9aca-402a-94a9-50f9c82999ae" name="Sec_in" connectedTo="2fa55afc-fa8c-4ce6-8ea4-c76de866cdd5" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:OutPort" id="45d1b11f-f190-4f0b-a7ec-f5f05e84b8bd" name="Sec_out" connectedTo="8d79c71e-8c27-4c6e-afa2-eeda757964bb" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="460a413a-e859-43ba-93de-6686db27d7ee" name="Pipe_460a" length="209.65">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.080704870213225" lon="5.192890179977971"/>
          <point xsi:type="esdl:Point" lat="52.08073280276776" lon="5.195957859025557"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="8d79c71e-8c27-4c6e-afa2-eeda757964bb" name="In" connectedTo="45d1b11f-f190-4f0b-a7ec-f5f05e84b8bd" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="bf07b1f9-8aad-4edd-b37f-00a8b137e3df" name="Out" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf" connectedTo="aca71b0d-d824-4bb5-90e3-7867737e94f3"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="bf6ba8c6-6c1a-48ad-8b5c-2a8596f86318" name="Pipe_bf6b" length="194.26">
        <geometry xsi:type="esdl:Line">
          <point xsi:type="esdl:Point" lat="52.07967150314069" lon="5.19577466391108"/>
          <point xsi:type="esdl:Point" lat="52.07962329969199" lon="5.19293309374643"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="77027030-f3a6-41ed-b93b-53a9cfc871b1" name="In" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11" connectedTo="18bb0b73-2409-4ba2-a203-a16fbe24794a"/>
        <port xsi:type="esdl:OutPort" id="2fa55afc-fa8c-4ce6-8ea4-c76de866cdd5" name="Out" connectedTo="9e01177a-9aca-402a-94a9-50f9c82999ae" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="433481be-3e4d-41c1-a9fa-d4c120d2db9b" name="Pipe_4334" length="285.3">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.08068664039604" lon="5.198564887933751"/>
          <point xsi:type="esdl:Point" lat="52.080693232120964" lon="5.202739492336873"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="8480ec60-d504-4e09-816a-1b4f8d385cb1" name="In" carrier="092a45a6-b26d-46bb-a84e-72d5bdb6807c" connectedTo="79b1f5a6-088f-4849-b276-a158035a1a07"/>
        <port xsi:type="esdl:OutPort" id="b44203fe-8a7e-4f23-8242-34646d2ca97f" name="Out" carrier="092a45a6-b26d-46bb-a84e-72d5bdb6807c" connectedTo="850a4675-0c79-4b3a-9562-c8ae275b88ba"/>
      </asset>
      <asset xsi:type="esdl:Pipe" id="c314eaf1-749b-49a1-8413-7c47907b4a3e" name="Pipe_c314" length="282.4">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="52.07973082997912" lon="5.202803882122016"/>
          <point xsi:type="esdl:Point" lat="52.079704462505106" lon="5.1986722042423095"/>
        </geometry>
        <port xsi:type="esdl:InPort" id="a4bb1e29-342b-40b8-9794-2ffaa83dc18e" name="In" carrier="b589726f-3940-4a1f-b06c-488862a9c4c6" connectedTo="efcf3749-bb0d-4697-8d87-e39fae365c26"/>
        <port xsi:type="esdl:OutPort" id="9e857b32-4619-4263-86d5-25cda4a78836" name="Out" carrier="b589726f-3940-4a1f-b06c-488862a9c4c6" connectedTo="eb53a5bf-afe0-4976-911c-bf8e29b887e9"/>
      </asset>
      <asset xsi:type="esdl:HeatExchange" id="634c8157-1baa-4801-8779-da0f685f30c1" name="HeatExchange_634c">
        <geometry xsi:type="esdl:Point" lat="52.08023180902598" lon="5.197287823861819" CRS="WGS84"/>
        <port xsi:type="esdl:InPort" id="aca71b0d-d824-4bb5-90e3-7867737e94f3" name="PrimIn" connectedTo="bf07b1f9-8aad-4edd-b37f-00a8b137e3df" carrier="baeed7a3-22e7-43b4-ad3b-837aa0634daf"/>
        <port xsi:type="esdl:OutPort" id="18bb0b73-2409-4ba2-a203-a16fbe24794a" name="PrimOut" connectedTo="77027030-f3a6-41ed-b93b-53a9cfc871b1" carrier="7cd930ee-a18e-4783-a9cf-6d64bf298a11"/>
        <port xsi:type="esdl:InPort" id="eb53a5bf-afe0-4976-911c-bf8e29b887e9" name="SecIn" connectedTo="9e857b32-4619-4263-86d5-25cda4a78836" carrier="b589726f-3940-4a1f-b06c-488862a9c4c6"/>
        <port xsi:type="esdl:OutPort" id="79b1f5a6-088f-4849-b276-a158035a1a07" name="SecOut" connectedTo="8480ec60-d504-4e09-816a-1b4f8d385cb1" carrier="092a45a6-b26d-46bb-a84e-72d5bdb6807c"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="6955a3da-0f5d-4e9c-881d-685bb5f1a8c0">
    <carriers xsi:type="esdl:Carriers" id="6e43055a-a009-462f-8f29-91ade19b0a8c">
      <carrier xsi:type="esdl:HeatCommodity" id="497f44b0-cfe3-4c87-862c-492f9339c261" name="HeatSupplyprim" supplyTemperature="50.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b34bc6ff-0f30-48d9-8604-9e9db1e34934" name="HeatReturnprim" returnTemperature="40.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="baeed7a3-22e7-43b4-ad3b-837aa0634daf" name="HeatSupplysec" supplyTemperature="70.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="7cd930ee-a18e-4783-a9cf-6d64bf298a11" name="HeatReturnsec" returnTemperature="60.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="092a45a6-b26d-46bb-a84e-72d5bdb6807c" name="HeatHexSecSupply" supplyTemperature="55.0"/>
      <carrier xsi:type="esdl:HeatCommodity" id="b589726f-3940-4a1f-b06c-488862a9c4c6" name="HeatHexSecRet" returnTemperature="50.0"/>
    </carriers>
    <quantityAndUnits xsi:type="esdl:QuantityAndUnits" id="774562e8-aec5-4ff4-9efc-63bb45437f10">
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="12c481c0-f81e-49b6-9767-90457684d24a" description="Energy in kWh" physicalQuantity="ENERGY" multiplier="KILO" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="93aa23ea-4c5d-4969-97d4-2a4b2720e523" description="Energy in MWh" physicalQuantity="ENERGY" multiplier="MEGA" unit="WATTHOUR"/>
      <quantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="e9405fc8-5e57-4df5-8584-4babee7cdf1b" description="Power in MW" physicalQuantity="POWER" multiplier="MEGA" unit="WATT"/>
    </quantityAndUnits>
  </energySystemInformation>
</esdl:EnergySystem>
